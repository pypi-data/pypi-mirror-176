import torch
import torch.nn as nn
from torch.nn import functional as F
from typing import Union
import pathlib
import einops
import einops.layers.torch
import math

import retinapy
import retinapy.mea as mea
import retinapy.nn

import logging

_logger = logging.getLogger(__name__)


def load_model(
    model, checkpoint_path: Union[str, pathlib.Path], map_location=None
):
    checkpoint_path = pathlib.Path(checkpoint_path)
    if not checkpoint_path.exists():
        raise FileNotFoundError(
            f"Checkpoint file/folder ({checkpoint_path}) not found."
        )
    if checkpoint_path.is_dir():
        checkpoint_path = list(checkpoint_path.glob("*.pth"))[-1]

    _logger.info(f"Loading model from ({checkpoint_path}).")
    checkpoint_state = torch.load(checkpoint_path, map_location)
    model_state = checkpoint_state["model"]
    model.load_state_dict(model_state)

def load_model_and_optimizer(
    model, optimizer, checkpoint_path: Union[str, pathlib.Path]):
    checkpoint_path = pathlib.Path(checkpoint_path)
    if not checkpoint_path.exists():
        raise FileNotFoundError(
            f"Checkpoint file/folder ({checkpoint_path}) not found."
        )
    if checkpoint_path.is_dir():
        checkpoint_path = list(checkpoint_path.glob("*.pth"))[-1]

    _logger.info(f"Loading model from ({checkpoint_path}).")
    checkpoint_state = torch.load(checkpoint_path)
    model_state = checkpoint_state["model"]
    model.load_state_dict(model_state)
    optimizer.load_state_dict(checkpoint_state["optimizer"])


def save_model(model, path: pathlib.Path, optimizer=None):
    _logger.info(f"Saving model to ({path})")
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    state = {
        "model": model.state_dict(),
    }
    if optimizer:
        state.update({"optimizer": optimizer.state_dict()})
    torch.save(state, path)


def dist_loss(prediction, target):
    """
    MSE loss reduced along time dimension but not batch dimension.

    It is expected that this loss is just one part of a loss term, so reducing
    over the batch dimension is not done. And it's not even given as a option
    as it's too easy to mistake "mean" reduction to be over a single dimension,
    when it is a full reduction over all dimensions. This is a tricky aspect of
    PyTorch's MSE loss.
    """
    # Scale to get roughly in the ballpark of 0.1 to 10.
    DIST_LOSS_SCALE = 3
    loss = DIST_LOSS_SCALE * F.mse_loss(prediction, target, reduction="none")
    assert len(prediction.shape) == 2, "Batch and time dim expected."
    time_ave = torch.mean(loss, dim=1)
    batch_sum = torch.sum(time_ave)
    return batch_sum


class DistLossLinear(nn.Module):
    def __init__(self, alpha=0.1, beta=0.01):
        super().__init__()
        self.alpha = alpha
        self.beta = beta

    def forward(self, prediction, target):
        # In some sense, the target is never 0. A best estimate is that it's
        # closer to this time value than the previous or next. In expectation,
        # the distance will be 0.25 away from this time point, with a
        # uniform prior.
        error = F.l1_loss(prediction, target)
        scaling = self.alpha + 1 / (self.beta + target)
        loss = torch.mean(error * scaling)
        return loss


class IntervalWeightedDistLoss(nn.Module):
    def __init__(self, alpha=0.1, beta=0.05):
        super(IntervalWeightedDistLoss, self).__init__()
        self.alpha = alpha
        self.beta = beta

    def forward(self, prediction, target, interval):
        error = F.l1_loss(prediction, target)
        scaling = self.alpha + 1 / (self.beta + interval)
        loss = torch.mean(error * scaling)
        return loss


class FcModel(nn.Module):
    def __init__(self, in_n, out_n, clamp_max):
        super(FcModel, self).__init__()
        self.clamp_max = clamp_max
        self.fc_body = retinapy.nn.FcBlock(
            hidden_ch=1024 * 2,
            num_hidden_layers=5,
            in_features=in_n,
            out_features=out_n,
            outermost_linear=True,
        )
        self.act = torch.nn.Softplus()

    def forward(self, x):
        x = self.act(self.fc_body(x))
        x = torch.clamp(x, min=None, max=self.clamp_max)
        return x


class MiniVAE(nn.Module):
    def __init__(self, num_clusters, z_n=2):
        super(MiniVAE, self).__init__()
        self.embed_mu = nn.Embedding(num_clusters, z_n)
        self.embed_logvar = nn.Embedding(num_clusters, z_n)

    def encode(self, x):
        x = x.long()
        mu = self.embed_mu(x)
        logvar = self.embed_logvar(x)
        return mu, logvar

    def sampling(self, mu, logvar):
        std = logvar.mul(0.5).exp_()
        eps = std.new_empty(std.size()).normal_()
        return eps.mul_(std).add_(mu)

    def forward(self, x):
        z_mu, z_logvar = self.encode(x)
        if self.training:
            z = self.sampling(z_mu, z_logvar)
        else:
            z = z_mu
        return z, z_mu, z_logvar


class VAE(nn.Module):
    def __init__(self, num_clusters, z_n=2, h1_n=16, h2_n=32, out_n=5):
        super(VAE, self).__init__()
        self.embed_mu = nn.Embedding(num_clusters, z_n)
        self.embed_logvar = nn.Embedding(num_clusters, z_n)
        self.fc1 = nn.Linear(z_n, h1_n)
        self.fc2 = nn.Linear(h1_n, h2_n)
        self.fc3 = nn.Linear(h2_n + z_n, out_n)

    def encode(self, x):
        x = x.long()
        mu = self.embed_mu(x)
        logvar = self.embed_logvar(x)
        return mu, logvar

    def sampling(self, mu, logvar):
        std = logvar.mul(0.5).exp_()
        eps = std.new_empty(std.size()).normal_()
        return eps.mul_(std).add_(mu)

    def decode(self, z):
        """
        Trying out skip connections, due to positive results reported here:
             https://adjidieng.github.io/Papers/skipvae.pdf
        """
        h1 = F.relu(self.fc1(z))
        h2 = F.relu(self.fc2(h1))
        h2_skip = torch.cat([h2, z], dim=1)
        return self.fc3(h2_skip)

    def forward(self, x):
        z_mu, z_logvar = self.encode(x)
        if self.training:
            z = self.sampling(z_mu, z_logvar)
        else:
            z = z_mu
        return self.decode(z), z_mu, z_logvar


class QueryDecoder(nn.Module):
    def __init__(self, n_z, num_queries, key_len, n_hidden1=30, n_hidden2=30):
        super().__init__()
        self.out_shape = (num_queries, key_len)
        self.fc1 = nn.Linear(n_z, n_hidden1)
        self.fc2 = nn.Linear(n_hidden1, n_hidden2)
        self.fc3 = nn.Linear(n_hidden2, num_queries * key_len)

    def forward(self, z):
        x = torch.tanh(self.fc1(z))
        x = torch.tanh(self.fc2(x))
        x = self.fc3(x)
        x = x.view(-1, *self.out_shape)
        return x


class MultiClusterModel2(nn.Module):
    LED_CHANNELS = 4
    NUM_CLUSTERS = 1

    def __init__(
        self, in_len, out_len, num_downsample, num_recordings, num_clusters
    ):
        super().__init__()
        self.in_len = in_len
        self.out_len = out_len
        self.num_input_channels = self.LED_CHANNELS + self.NUM_CLUSTERS
        # Linear
        self.linear_in_len = 1 + (in_len - 1) // (2**num_downsample)

        self.num_channels = [20, 100, 100, 100]
        self.downsample = [False, False, True, False]
        self.num_repeats = [None, 2, num_downsample - 1, 3]
        self.mid_kernel_size = 7
        self.kernel_sizes = [
            51,
            self.mid_kernel_size,
            self.mid_kernel_size,
            self.mid_kernel_size,
        ]
        self.expansion = 1
        # VAE
        self.z_dim = 2
        self.num_clusters = num_clusters
        self.num_embed = num_recordings * num_clusters
        self.n_h1 = 20
        self.n_h2 = 20
        # HyperResnet
        warehouse_size = 1500
        self.key_len = 16  # 32 = ~ sqrt(1000)

        # Huge memory store.
        self.warehouse = retinapy.nn.Conv1dWarehouse(
            max_in_channels=1,  # depth-wise conv.
            warehouse_size=warehouse_size,
            kernel_size=self.mid_kernel_size,
            key_len=self.key_len,
        )

        # Traditional conv layers.
        self.layer0 = nn.Sequential(
            nn.Conv1d(
                self.num_input_channels,
                self.num_channels[0],
                kernel_size=self.kernel_sizes[0],
                stride=2,
                padding=self.kernel_sizes[0] // 2,
                bias=True,
            ),
            nn.LeakyReLU(0.2, True),
            nn.Conv1d(
                self.num_channels[0],
                self.num_channels[0],
                kernel_size=self.kernel_sizes[0],
                stride=1,
                padding=self.kernel_sizes[0] // 2,
                bias=False,
            ),
            retinapy.nn.create_batch_norm(self.num_channels[0]),
            nn.LeakyReLU(0.2, True),
        )

        mid = []
        total_num_channels = 0
        for layer_idx in range(1, len(self.num_channels)):
            blocks = []
            for i in range(self.num_repeats[layer_idx]):
                num_in = (
                    self.num_channels[layer_idx - 1]
                    if (i == 0)
                    else self.num_channels[layer_idx]
                )
                res_block_F = retinapy.nn.ResBlock1d_F(
                    num_in,
                    self.num_channels[layer_idx] * self.expansion,
                    self.num_channels[layer_idx],
                    kernel_size=self.kernel_sizes[layer_idx],
                    downsample=self.downsample[layer_idx],
                )
                blocks.append(res_block_F)
                total_num_channels += res_block_F.num_channels()
            mid.append(nn.ModuleList(blocks))
        self.mid_layers = nn.ModuleList(mid)

        # Back to traditional conv layers.
        self.layer4 = nn.Conv1d(
            in_channels=self.num_channels[-1],
            out_channels=1,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=True,
        )
        linear_in_len = 1 + (in_len - 1) // (2**num_downsample)
        self.linear = nn.Linear(
            in_features=linear_in_len,
            out_features=self.out_len,
        )
        # VAE
        self.vae = MiniVAE(num_recordings * num_clusters, z_n=self.z_dim)
        # VAE decode to attention query
        # 1 query per mid channel.
        self.query_decoder = QueryDecoder(
            self.z_dim, total_num_channels, self.key_len
        )

    def encode_vae(self, rec_id, cluster_id):
        id_ = rec_id * self.num_clusters + cluster_id
        z, z_mu, z_logvar = self.vae(id_)
        return z, z_mu, z_logvar

    def forward(self, snippet, rec_id, cluster_id):
        # Layer 0
        x = self.layer0(snippet)
        # VAE
        z, z_mu, z_logvar = self.encode_vae(rec_id, cluster_id)
        # Queries
        queries = self.query_decoder(z)
        weights_W, weights_b = self.warehouse(queries)
        idx_start = 0
        for module_list in self.mid_layers:
            for layer in module_list:
                x, idx_start = layer.forward(x, weights_W, weights_b, idx_start)
        x = self.layer4(x)
        x = self.linear(torch.flatten(x, start_dim=1))
        return x, z_mu, z_logvar


class CatMultiClusterModel(nn.Module):
    LED_CHANNELS = 4
    NUM_CLUSTERS = 1

    def __init__(
        self,
        in_len,
        out_len,
        num_downsample,
        num_recordings,
        num_clusters,
        z_dim=2,
    ):
        super().__init__()
        self.in_len = in_len
        self.out_len = out_len
        # led_channels, mean(led_channels), num_clusters, pos_encoding
        self.num_input_channels = self.LED_CHANNELS * 2 + self.NUM_CLUSTERS + 1
        # Linear
        self.linear_in_len = 1 + (in_len - 1) // (2**num_downsample)
        # L1
        self.l0_num_channels = 50
        # CNN parameters
        self.num_l1_blocks = num_downsample - 1
        self.num_l2_blocks = 3
        self.expansion = 2
        self.l1_num_channels = 100
        self.l2_num_channels = 200
        kernel_size = 21
        mid_kernel_size = 7
        # VAE
        self.z_dim = z_dim
        self.num_recordings = num_recordings
        self.num_clusters = num_clusters
        self.n_vae_out = 30

        self.layer0 = nn.Sequential(
            nn.Conv1d(
                self.num_input_channels,
                self.l0_num_channels,
                kernel_size=kernel_size,
                stride=2,
                padding=kernel_size // 2,
                bias=True,
            ),
            nn.LeakyReLU(0.2, True),
            nn.Conv1d(
                self.l0_num_channels,
                self.l0_num_channels,
                kernel_size=kernel_size,
                stride=1,
                padding=kernel_size // 2,
                bias=False,
            ),
            retinapy.nn.create_batch_norm(self.l0_num_channels),
            nn.LeakyReLU(0.2, True),
        )

        l1_blocks = []
        l1_num_in = self.l0_num_channels + self.n_vae_out
        for i in range(self.num_l1_blocks):
            num_in = self.l1_num_channels if i else l1_num_in
            l1_blocks.append(
                retinapy.nn.ResBlock1d(
                    num_in,
                    self.l1_num_channels * self.expansion,
                    self.l1_num_channels,
                    kernel_size=mid_kernel_size,
                    downsample=True,
                ),
            )
        self.layer1 = nn.Sequential(*l1_blocks)
        l2_blocks = []
        for i in range(self.num_l1_blocks):
            num_in = self.l2_num_channels if i else self.l1_num_channels
            l2_blocks.append(
                retinapy.nn.ResBlock1d(
                    num_in,
                    self.l2_num_channels * self.expansion,
                    self.l2_num_channels,
                    kernel_size=mid_kernel_size,
                    downsample=False,
                ),
            )
        self.layer2 = nn.Sequential(*l2_blocks)

        self.layer3 = nn.Conv1d(
            in_channels=self.l2_num_channels,
            out_channels=1,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=True,
        )

        linear_in_len = 1 + (in_len - 1) // (2**num_downsample)
        self.linear = nn.Linear(
            in_features=linear_in_len,
            out_features=self.out_len,
        )
        # VAE
        self.vae = VAE(
            num_recordings * num_clusters, z_n=self.z_dim, out_n=self.n_vae_out
        )

    def encode_vae(self, rec_id, cluster_id):
        id_ = rec_id * self.num_clusters + cluster_id
        z_decode, z_mu, z_logvar = self.vae(id_)
        return z_decode, z_mu, z_logvar

    # def cat_downsample(self, x):
    #     ds = torchaudio.functional.lowpass_biquad(
    #             x[:,0:-1], sample_rate=992, cutoff_freq=10, Q=0.707
    #     )
    #     x = torch.cat([x, ds], dim=1)
    #     return x

    def cat_mean(self, snippet):
        m = (
            snippet[:, 0 : mea.NUM_STIMULUS_LEDS]
            .mean(dim=2, keepdim=True)
            .expand(-1, -1, snippet.shape[-1])
        )
        x = torch.cat([snippet, m], dim=1)
        return x

    def cat_z(self, x, z):
        z = z.unsqueeze(-1).expand(-1, -1, x.shape[-1])
        x = torch.cat([x, z], dim=1)
        return x

    def forward(self, snippet, rec_id, cluster_id):
        # VAE
        x = self.cat_mean(snippet)
        x = self.layer0(x)
        z_decode, z_mu, z_logvar = self.encode_vae(rec_id, cluster_id)
        x = self.cat_z(x, z_decode)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.linear(torch.flatten(x, start_dim=1))
        return x, z_mu, z_logvar


class MultiClusterModel(nn.Module):
    LED_CHANNELS = 4
    NUM_CLUSTERS = 1

    def __init__(
        self,
        in_len,
        out_len,
        num_downsample,
        num_recordings,
        num_clusters,
        z_dim=2,
    ):
        super(MultiClusterModel, self).__init__()
        self.in_len = in_len
        self.out_len = out_len
        # led_channels, mean(led_channels), num_clusters, pos_encoding
        self.num_input_channels = self.LED_CHANNELS * 2 + self.NUM_CLUSTERS + 1
        # Linear
        self.linear_in_len = 1 + (in_len - 1) // (2**num_downsample)
        # L1
        self.l0_num_channels = 50
        self.l1_num_channels = 50
        # CNN parameters
        self.num_l1_blocks = 1
        self.num_l2_blocks = num_downsample - 1
        self.num_l3_blocks = 1
        self.expansion = 1
        self.l2_num_channels = 100
        self.l3_num_channels = 200
        kernel_size = 21
        mid_kernel_size = 7
        # VAE
        self.z_dim = z_dim
        self.num_recordings = num_recordings
        self.num_clusters = num_clusters
        # HyperResnet
        warehouse_factor = 8
        self.hyper_hidden1 = 16
        self.hyper_hidden2 = 16

        self.layer0 = nn.Sequential(
            nn.Conv1d(
                self.num_input_channels,
                self.l0_num_channels,
                kernel_size=kernel_size,
                stride=2,
                padding=kernel_size // 2,
                bias=True,
            ),
            nn.LeakyReLU(0.2, True),
            nn.Conv1d(
                self.l0_num_channels,
                self.l0_num_channels,
                kernel_size=kernel_size,
                stride=1,
                padding=kernel_size // 2,
                bias=False,
            ),
            retinapy.nn.create_batch_norm(self.l0_num_channels),
            nn.LeakyReLU(0.2, True),
        )
        l1_blocks = []
        for i in range(self.num_l1_blocks):
            num_in = self.l1_num_channels if i else self.l0_num_channels
            hyper_res_block = retinapy.nn.HyperResBlock1d(
                num_in,
                self.l1_num_channels * self.expansion,
                self.l1_num_channels,
                warehouse_factor=warehouse_factor,
                kernel_size=mid_kernel_size,
                downsample=False,
            )
            hyper_decoder = retinapy.nn.HyperResDecoder(
                hyper_res_block,
                in_n=self.z_dim,
                hidden1_n=self.hyper_hidden1,
                hidden2_n=self.hyper_hidden2,
            )
            l1_blocks.append(hyper_decoder)
        self.layer1 = nn.ModuleList(l1_blocks)

        l2_blocks = []
        for i in range(self.num_l2_blocks):
            num_in = self.l2_num_channels if i else self.l1_num_channels
            l2_blocks.append(
                retinapy.nn.ResBlock1d(
                    num_in,
                    self.l2_num_channels * self.expansion,
                    self.l2_num_channels,
                    kernel_size=mid_kernel_size,
                    downsample=True,
                ),
            )
        self.layer2 = nn.Sequential(*l2_blocks)

        l3_blocks = []
        for i in range(self.num_l3_blocks):
            num_in = self.l3_num_channels if i else self.l2_num_channels
            hyper_res_block = retinapy.nn.HyperResBlock1d(
                num_in,
                self.l3_num_channels * self.expansion,
                self.l3_num_channels,
                warehouse_factor=warehouse_factor,
                kernel_size=mid_kernel_size,
                downsample=False,
            )
            hyper_decoder = retinapy.nn.HyperResDecoder(
                hyper_res_block,
                in_n=self.z_dim,
                hidden1_n=self.hyper_hidden1,
                hidden2_n=self.hyper_hidden2,
            )
            l3_blocks.append(hyper_decoder)
        self.layer3 = nn.ModuleList(l3_blocks)
        self.layer4 = nn.Conv1d(
            in_channels=self.l3_num_channels,
            out_channels=1,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=True,
        )
        linear_in_len = 1 + (in_len - 1) // (2**num_downsample)
        self.linear = nn.Linear(
            in_features=linear_in_len,
            out_features=self.out_len,
        )
        # VAE
        self.vae = MiniVAE(num_recordings * num_clusters, z_n=self.z_dim)

    def encode_vae(self, rec_id, cluster_id):
        id_ = rec_id * self.num_clusters + cluster_id
        z, z_mu, z_logvar = self.vae(id_)
        return z, z_mu, z_logvar

    # def cat_downsample(self, x):
    #     ds = torchaudio.functional.lowpass_biquad(
    #             x[:,0:-1], sample_rate=992, cutoff_freq=10, Q=0.707
    #     )
    #     x = torch.cat([x, ds], dim=1)
    #     return x

    def cat_mean(self, snippet):
        m = (
            snippet[:, 0:-1]
            .mean(dim=2, keepdim=True)
            .expand(-1, -1, snippet.shape[-1])
        )
        x = torch.cat([snippet, m], dim=1)
        return x

    def forward(self, snippet, rec_id, cluster_id):
        x = self.cat_mean(snippet)
        x = self.layer0(x)
        # VAE
        z, z_mu, z_logvar = self.encode_vae(rec_id, cluster_id)
        # Hyper
        for l in self.layer1:
            x = l(x, z)
        x = self.layer2(x)
        for l in self.layer3:
            x = l(x, z)
        x = self.layer4(x)
        x = self.linear(torch.flatten(x, start_dim=1))
        return x, z_mu, z_logvar


class ClusteringTransformer(nn.Module):
    def __init__(
        self, in_len, out_len, stim_downsample, num_recordings, num_clusters,
        z_dim=2, num_heads=8, head_dim=64, num_tlayers=6):
        super().__init__()
        self.in_len = in_len
        self.num_recordings = num_recordings
        self.num_clusters = num_clusters
        self.z_dim = z_dim
        # Stimulus CNN
        k0_size = 21
        k1_size = 7
        expansion = 1
        self.l0a_num_channels = 10
        self.l0b_num_channels = 20
        self.l1_num_channels = 100
        self.cnn = nn.Sequential(
            nn.Conv1d(
                mea.NUM_STIMULUS_LEDS * 2,  # stimulus + mean(stimulus)
                self.l0a_num_channels,
                kernel_size=k0_size,
                stride=2,
                padding=(k0_size - 1) // 2,
                bias=True,
            ),
            nn.LeakyReLU(0.2, True),
            nn.Conv1d(
                self.l0a_num_channels,
                self.l0b_num_channels,
                kernel_size=k0_size,
                stride=1,
                padding=(k0_size - 1) // 2,
                bias=False,
            ),
            retinapy.nn.create_batch_norm(self.l0b_num_channels),
            nn.LeakyReLU(0.2, True),
            *[
                retinapy.nn.ResBlock1d(
                    self.l1_num_channels if i else self.l0b_num_channels,
                    self.l1_num_channels * expansion,
                    self.l1_num_channels,
                    kernel_size=k1_size,
                    downsample=True,
                )
                for i in range(stim_downsample - 1)
            ],
        )
        
        self.embed_dim = 128
        # VAE
        self.vae = VAE(
            self.num_recordings * self.num_clusters, 
            z_n=self.z_dim, 
            h1_n=32,
            h2_n=32,
            out_n=self.embed_dim)
        # Transformer
        self.stim_embed = nn.Conv1d(
            self.l1_num_channels, self.embed_dim, kernel_size=1
        )
        # Normally initialized nn.Parameter
        # 1092 = 992 + 100
        in_stim_len = self.in_len + out_len
        enc_stim_len = 1 + (in_stim_len - 1) // (2**stim_downsample)
        enc_len = enc_stim_len + 1 # 1 for VAE encoding.
        self.pos_embed = nn.Parameter(torch.randn(enc_len, self.embed_dim))

        mlp_expansion = 3
        self.transformer = retinapy.nn.Transformer(
            self.embed_dim,
            num_layers=num_tlayers,
            num_heads=num_heads,
            head_dim=head_dim,
            mlp_dim=self.embed_dim * mlp_expansion,
        )
        self.decode = nn.Sequential(
            nn.Linear(self.embed_dim, 1),
            einops.layers.torch.Rearrange("b c 1 -> b c"),
            nn.Linear(enc_len, out_len),
        )

    def cat_mean(self, stim):
        m = (
            stim[:, 0 : mea.NUM_STIMULUS_LEDS]
            .mean(dim=2, keepdim=True)
            .expand(-1, -1, stim.shape[-1])
        )
        x = torch.cat([stim, m], dim=1)
        return x

    def encode_stimulus(self, stim):
        x = self.cat_mean(stim)
        x = self.cnn(x)
        x = self.stim_embed(x)
        x = einops.rearrange(x, "b c l -> b l c")
        return x

    def encode_vae(self, rec_id, cluster_id):
        id_ = rec_id * self.num_clusters + cluster_id
        z_decode, z_mu, z_logvar = self.vae(id_)
        return z_decode, z_mu, z_logvar

    def forward(self, snippet, rec_id, cluster_id):
        z_decode, z_mu, z_logvar = self.encode_vae(rec_id, cluster_id)
        x_stim = self.encode_stimulus(snippet[:, 0:-1])
        z = einops.rearrange(z_decode, "b c -> b () c")
        x = torch.cat([x_stim, z], dim=1)
        x = x + self.pos_embed
        x = self.transformer(x)
        x = self.decode(x)
        return x, z_mu, z_logvar

class TransformerModel(nn.Module):
    def __init__(
        self, in_len, out_len, stim_downsample, num_recordings, num_clusters,
        z_dim=2, num_heads=8, head_dim=64, num_tlayers=6, spike_patch_len=8):
        super().__init__()
        self.in_len = in_len
        self.num_recordings = num_recordings
        self.num_clusters = num_clusters
        self.z_dim = z_dim
        # Stimulus CNN
        k0_size = 21
        k1_size = 7
        expansion = 1
        self.l0a_num_channels = 10
        self.l0b_num_channels = 20
        self.l1_num_channels = 100
        self.cnn = nn.Sequential(
            nn.Conv1d(
                mea.NUM_STIMULUS_LEDS * 2,  # stimulus + mean(stimulus)
                self.l0a_num_channels,
                kernel_size=k0_size,
                stride=2,
                padding=(k0_size - 1) // 2,
                bias=True,
            ),
            nn.LeakyReLU(0.2, True),
            nn.Conv1d(
                self.l0a_num_channels,
                self.l0b_num_channels,
                kernel_size=k0_size,
                stride=1,
                padding=(k0_size - 1) // 2,
                bias=False,
            ),
            retinapy.nn.create_batch_norm(self.l0b_num_channels),
            nn.LeakyReLU(0.2, True),
            *[
                retinapy.nn.ResBlock1d(
                    self.l1_num_channels if i else self.l0b_num_channels,
                    self.l1_num_channels * expansion,
                    self.l1_num_channels,
                    kernel_size=k1_size,
                    downsample=True,
                )
                for i in range(stim_downsample - 1)
            ],
        )
        
        self.embed_dim = 128
        # VAE
        self.vae = VAE(
            self.num_recordings * self.num_clusters, 
            z_n=self.z_dim, 
            h1_n=32,
            h2_n=32,
            out_n=self.embed_dim)
        # Transformer
        self.spike_patch_len = spike_patch_len
        self.stim_embed = nn.Conv1d(
            self.l1_num_channels, self.embed_dim, kernel_size=1
        )
        # Normally initialized nn.Parameter
        # 1092 = 992 + 100
        in_stim_len = self.in_len + out_len
        enc_stim_len = 1 + (in_stim_len - 1) // (2**stim_downsample)
        enc_spikes_len = math.ceil(self.in_len // self.spike_patch_len)
        self.spike_pad = enc_spikes_len * self.spike_patch_len - self.in_len
        enc_len = enc_stim_len + enc_spikes_len + 1 # 1 for VAE encoding.
        self.pos_embed = nn.Parameter(torch.randn(enc_len, self.embed_dim))

        self.spikes_embed = nn.Linear(self.spike_patch_len, self.embed_dim)
        mlp_expansion = 3
        self.transformer = retinapy.nn.Transformer(
            self.embed_dim,
            num_layers=num_tlayers,
            num_heads=num_heads,
            head_dim=head_dim,
            mlp_dim=self.embed_dim * mlp_expansion,
        )
        self.decode = nn.Sequential(
            nn.Linear(self.embed_dim, 1),
            einops.layers.torch.Rearrange("b c 1 -> b c"),
            nn.Linear(enc_len, out_len),
        )

    def cat_mean(self, stim):
        m = (
            stim[:, 0 : mea.NUM_STIMULUS_LEDS]
            .mean(dim=2, keepdim=True)
            .expand(-1, -1, stim.shape[-1])
        )
        x = torch.cat([stim, m], dim=1)
        return x

    def encode_stimulus(self, stim):
        x = self.cat_mean(stim)
        x = self.cnn(x)
        x = self.stim_embed(x)
        x = einops.rearrange(x, "b c l -> b l c")
        return x

    def encode_spikes(self, spikes):
        # Pad the spikes to be a multiple of the patch length.
        # Pad on the left, as the left has less of an effect on the output.
        x = F.pad(spikes, (self.spike_pad, 0))
        x = einops.rearrange(x, "b (t c) -> b t c", c=self.spike_patch_len)
        x = self.spikes_embed(x)
        return x

    def encode_vae(self, rec_id, cluster_id):
        id_ = rec_id * self.num_clusters + cluster_id
        z_decode, z_mu, z_logvar = self.vae(id_)
        return z_decode, z_mu, z_logvar

    def forward(self, snippet, rec_id, cluster_id):
        z_decode, z_mu, z_logvar = self.encode_vae(rec_id, cluster_id)
        x_stim = self.encode_stimulus(snippet[:, 0:-1])
        x_spikes = self.encode_spikes(snippet[:, -1][:, : self.in_len])
        z = einops.rearrange(z_decode, "b c -> b () c")
        x = torch.cat([x_stim, x_spikes, z], dim=1)
        x = x + self.pos_embed
        x = self.transformer(x)
        x = self.decode(x)
        return x, z_mu, z_logvar


class DistanceFieldCnnModel(nn.Module):
    LED_CHANNELS = 4
    NUM_CLUSTERS = 1

    def __init__(self, in_len, out_len):
        super(DistanceFieldCnnModel, self).__init__()
        self.in_len = in_len
        self.out_len = out_len
        # led_channels, mean(led_channels), num_clusters 
        self.num_input_channels = self.LED_CHANNELS * 2 + self.NUM_CLUSTERS
        self.l1_num_channels = 50
        self.l2_num_channels = 50
        self.l3_num_channels = 100
        kernel_size = 21
        mid_kernel_size = 7
        self.layer0 = nn.Sequential(
            nn.Conv1d(
                self.num_input_channels,
                self.l1_num_channels,
                kernel_size=kernel_size,
                stride=2,
                padding=(kernel_size - 1) // 2,
                bias=True,
            ),
            nn.LeakyReLU(0.2, True),
            nn.Conv1d(
                self.l1_num_channels,
                self.l1_num_channels,
                kernel_size=kernel_size,
                stride=1,
                padding=(kernel_size - 1) // 2,
                bias=False,
            ),
            retinapy.nn.create_batch_norm(self.l1_num_channels),
            nn.LeakyReLU(0.2, True),
        )
        self.layer1 = nn.Sequential(
            retinapy.nn.ResBlock1d(
                self.l1_num_channels,
                self.l2_num_channels,
                self.l2_num_channels,
                kernel_size=mid_kernel_size,
                downsample=False,
            ),
        )
        self.layer2_elements = []
        expansion = 1
        num_halves = 3  # There is 1 other downsamples other than the midlayers.
        for i in range(num_halves - 1):
            self.layer2_elements.append(
                retinapy.nn.ResBlock1d(
                    self.l2_num_channels,
                    self.l2_num_channels * expansion,
                    self.l2_num_channels,
                    kernel_size=mid_kernel_size,
                    downsample=True,
                )
            )
        self.layer2 = nn.Sequential(*self.layer2_elements)
        self.layer3 = retinapy.nn.ResBlock1d(
            self.l2_num_channels,
            self.l3_num_channels,
            self.l3_num_channels,
            kernel_size=mid_kernel_size,
            downsample=False,
        )
        self.layer4 = nn.Conv1d(
            in_channels=self.l3_num_channels,
            out_channels=1,
            kernel_size=5,
            stride=1,
            padding=2,
            bias=True,
        )
        linear_in_len = 1 + (in_len - 1) // 2**num_halves
        self.linear = nn.Linear(
            in_features=linear_in_len,
            out_features=self.out_len,
        )

    def cat_mean(self, snippet):
        m = (
            snippet[:, 0 : mea.NUM_STIMULUS_LEDS]
            .mean(dim=2, keepdim=True)
            .expand(-1, -1, snippet.shape[-1])
        )
        x = torch.cat([snippet, m], dim=1)
        return x

    def forward(self, x):
        x = self.cat_mean(x)
        x = self.layer0(x)
        # Keep or leave out? Interested to see a justification either way.
        # x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.linear(torch.flatten(x, start_dim=1))
        # Alternative parameter free head:
        # x = torch.squeeze(F.adaptive_avg_pool1d(x, output_size=self.out_len), dim=1)
        return x


class DistFieldToSpikeModel(nn.Module):
    def __init__(self, in_len):
        super(DistFieldToSpikeModel, self).__init__()
        self.act = nn.Softplus()
        k = 5
        c = 50
        n = 3
        self.layer1 = nn.Sequential(
            retinapy.nn.ResBlock1d(1, c, c, kernel_size=k, downsample=True),
            *[
                retinapy.nn.ResBlock1d(
                    c,
                    c,
                    c,
                    kernel_size=k,
                    downsample=True,
                )
                for _ in range(n - 1)
            ],
        )
        linear_in_len = (in_len // 2**n) * c
        self.linear = nn.Linear(in_features=linear_in_len, out_features=1)

    def forward(self, x):
        x = x.unsqueeze(dim=1)
        x = self.layer1(x)
        x = self.linear(torch.flatten(x, start_dim=1))
        x = self.act(x)
        x = torch.squeeze(x, dim=1)
        return x


class LinearNonlinear(nn.Module):
    # TODO: add options for 'rbf' and  'psp' activations.

    def __init__(self, in_n, out_n):
        super(LinearNonlinear, self).__init__()
        self.linear = nn.Linear(in_features=in_n, out_features=out_n)
        self.act = nn.Softplus()

    def forward(self, x):
        x = torch.flatten(x, start_dim=1)
        x = self.linear(x)
        x = self.act(x)
        # Remove the last dimension, as it is always 1.
        assert x.shape[1] == 1
        x = torch.squeeze(x, dim=1)
        return x


class DeepRetina2016(nn.Module):
    """
    From:
        https://github.com/baccuslab/deep-retina/blob/master/deepretina/models.py
    """

    def __init__(self, in_len, in_n, out_n):
        super(DeepRetina2016, self).__init__()
        self.in_n = in_n
        self.out_n = out_n
        self.in_len = in_len

        self.conv1 = nn.Conv2d(
            in_channels=self.in_n, out_channels=16, kernel_size=15
        )
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=8, kernel_size=9)
        linear_in_len = in_len - 15 + 1 - 9 + 1
        self.linear = nn.Linear(linear_in_len, self.out_n)
        self.act = nn.Softplus()
        # self.linear = nn.Linear(in_features=?, out_features=self.num_softmax_classes)

    def forward(self, x):
        # TODO: add noise?
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = torch.flatten(x, start_dim=1)
        x = self.linear(x)
        x = self.act(x)
