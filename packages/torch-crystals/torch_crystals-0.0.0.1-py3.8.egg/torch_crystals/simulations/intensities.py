from collections import defaultdict
from math import pi
from typing import Dict

import torch
from torch import Tensor

from crystals import Crystal

from .atom_factor import get_cmf, CromerMannFormula


class IntensityCalculator(object):
    def __init__(self, crystal: Crystal, device: torch.device = 'cuda', dtype: torch.dtype = torch.float64):
        self.dtype = dtype
        self.crystal = crystal
        self.device = device
        self.atom_dict = get_coords_atom_dict(crystal, self.device, self.dtype)
        self.cmf_dict = get_cmf_dict(crystal, self.device, self.dtype)

    def __call__(self, q_vectors: Tensor, miller_indices: Tensor):
        return self.calculate_intensities(q_vectors, miller_indices)

    def calculate_intensities(self, q_vectors: Tensor, miller_indices: Tensor):
        return calculate_intensities(q_vectors, self.cmf_dict, self.atom_dict, miller_indices)


def calculate_intensities(q_vectors: Tensor,
                          cmf_dict: Dict[str, CromerMannFormula],
                          atom_dict: Dict[str, Tensor],
                          miller_indices: Tensor
                          ) -> Tensor:
    sfs: Tensor = 0

    for el, coords in atom_dict.items():
        sfs += get_sf(cmf_dict[el], coords, q_vectors, miller_indices)

    return torch.abs(sfs) ** 2


def get_sf(cmf: CromerMannFormula, coords: Tensor, q_vectors: Tensor, miller_indices: Tensor) -> Tensor:
    ffs = cmf.get_ff(q_vectors)
    sf = ffs[..., None] * torch.exp(2 * pi * 1j * torch.einsum('ji,ki->jk', miller_indices, coords))
    return sf.sum(-1)


def get_cmf_dict(crystal: Crystal,
                 device: torch.device,
                 dtype: torch.dtype = torch.float64) -> Dict[str, CromerMannFormula]:
    elements = set(atom.element for atom in crystal)
    cmf_dict: Dict[str, CromerMannFormula] = {el: get_cmf(el, device=device, dtype=dtype) for el in elements}
    return cmf_dict


def get_coords_atom_dict(crystal: Crystal,
                         device: torch.device,
                         dtype: torch.dtype = torch.float64) -> Dict[str, Tensor]:
    atom_dict = defaultdict(list)
    tensor_dict: Dict[str, Tensor] = {}

    for atom in crystal:
        atom_dict[atom.element].append(atom.coords_fractional)
    for k, v in atom_dict.items():
        tensor_dict[k] = torch.tensor(v, dtype=dtype, device=device)
    return tensor_dict
