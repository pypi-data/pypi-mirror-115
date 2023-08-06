from typing import Iterable

import torch
from torch import Tensor


def to_np(arr):
    return arr.detach().cpu().numpy()


def to_t(t: Iterable, device: torch.device = 'cuda', dtype: torch.dtype = torch.float64) -> Tensor:
    if isinstance(t, Tensor):
        return t
    return torch.tensor(t, device=device, dtype=dtype)


@torch.jit.script
def length(t: Tensor) -> Tensor:
    return torch.sqrt((t ** 2).sum(-1))


@torch.jit.script
def norm(t: Tensor) -> Tensor:
    t_length = length(t)
    if t_length > 0:
        return t / t_length
    return t


@torch.jit.script
def get_2d_vector(vec: Tensor):
    return torch.stack([
        torch.sqrt(torch.sum(vec[..., :2] ** 2, dim=-1)),
        vec[..., 2],
    ], -1)
