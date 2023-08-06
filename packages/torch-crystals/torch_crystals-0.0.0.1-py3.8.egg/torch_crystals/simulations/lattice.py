import math

import torch
from torch import Tensor


@torch.jit.script
def lattice_vectors_from_parameters(params: Tensor):
    # stupid jit script does not understand otherwise :)
    rad = math.pi / 180
    a = params[0]
    b = params[1]
    c = params[2]
    alpha = params[3] * rad
    beta = params[4] * rad
    gamma = params[5] * rad

    # normal two-line version preceded by "from math import pi"
    # a, b, c = params[:3]
    # alpha, beta, gamma = params[3:] * pi / 180

    unit_volume = torch.sqrt(
        1.0
        + 2.0 * torch.cos(alpha) * torch.cos(beta) * torch.cos(gamma)
        - torch.cos(alpha) ** 2
        - torch.cos(beta) ** 2
        - torch.cos(gamma) ** 2
    )

    # reciprocal lattice
    a_recip = torch.sin(alpha) / (a * unit_volume)
    cos_gamma_recip = (
                              torch.cos(alpha) * torch.cos(beta) - torch.cos(gamma)
                      ) / (torch.sin(alpha) * torch.sin(beta))
    sin_gamma_recip = torch.sqrt(1 - cos_gamma_recip ** 2)

    a1 = torch.stack(
        [1 / a_recip, -cos_gamma_recip / sin_gamma_recip / a_recip, torch.cos(beta) * a],
    )
    zero = torch.tensor(0, device=params.device, dtype=params.dtype)
    a2 = torch.stack([zero, b * torch.sin(alpha), b * torch.cos(alpha)])
    a3 = torch.stack([zero, zero, c])

    return a1, a2, a3


@torch.jit.script
def calc_reciprocal_vectors(a1: Tensor, a2: Tensor, a3: Tensor) -> Tensor:
    unit_volume = torch.dot(a1, torch.cross(a2, a3))
    b1 = torch.cross(a2, a3)
    b2 = torch.cross(a3, a1)
    b3 = torch.cross(a1, a2)
    return torch.stack([b1, b2, b3]) * 2 * math.pi / unit_volume
