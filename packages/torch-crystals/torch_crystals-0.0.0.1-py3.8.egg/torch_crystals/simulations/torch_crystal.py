from crystals import Crystal

import torch
from torch import Tensor

from ..utils import to_t, length, get_2d_vector
from .lattice import lattice_vectors_from_parameters, calc_reciprocal_vectors
from .rotations import orientation_rotation_matrix
from .intensities import IntensityCalculator


class TorchCrystal(object):
    def __init__(self,
                 crystal: Crystal,
                 device: torch.device,
                 orientation: tuple = (0, 0, 1),
                 dtype: torch.dtype = torch.float64,
                 ):
        self.dtype = dtype
        self.crystal = crystal
        self.device = device
        self.intensity_calc = IntensityCalculator(self.crystal, self.device, self.dtype)
        self.a1, self.a2, self.a3 = None, None, None
        self.reciprocal, self.rot_mtx, self.reciprocal_mtx = None, None, None
        self.a, self.b, self.c, self.alpha, self.beta, self.gamma = to_t(
            self.crystal.lattice_parameters, device=self.device, dtype=self.dtype
        )
        self.orientation = to_t(orientation, dtype=self.dtype, device=self.device)
        self.update_mtx(update_rot=True)

    @property
    def params(self):
        return torch.stack([self.a, self.b, self.c, self.alpha, self.beta, self.gamma])

    def update_mtx(self, update_rot: bool = False):
        a1, a2, a3 = lattice_vectors_from_parameters(self.params)
        self.a1, self.a2, self.a3 = a1, a2, a3
        self.reciprocal = calc_reciprocal_vectors(a1, a2, a3)

        if update_rot:
            self.rot_mtx = orientation_rotation_matrix(self.orientation)

        self.reciprocal_mtx = (self.rot_mtx @ self.reciprocal.T).T

    def get_q_vectors(self, miller_indices: Tensor, mode: str = 'polar'):
        q_vectors = to_t(miller_indices) @ self.reciprocal_mtx

        if not mode:
            return q_vectors

        q_xy, q_z = get_2d_vector(q_vectors).T

        if mode == 'q_space':
            return q_xy, q_z

        q_mod = length(q_vectors)
        q_angle = torch.atan2(q_z, q_xy)
        return q_mod, q_angle
