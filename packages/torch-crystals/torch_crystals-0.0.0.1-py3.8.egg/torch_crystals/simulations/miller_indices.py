from itertools import product

import torch
from torch import Tensor
from torch import tensor


def get_miller_indices(idx_min: int, idx_max: int,
                       device: torch.device = 'cuda',
                       dtype: torch.dtype = torch.float64
                       ) -> Tensor:
    return tensor(
        _get_all_combinations(idx_min, idx_max),
        device=device, dtype=dtype,
    )


def _get_all_combinations(idx_min: int, idx_max: int):
    return list(filter(
        lambda x: any(x) != 0,
        product(list(range(idx_min, idx_max + 1)), repeat=3)
    ))
