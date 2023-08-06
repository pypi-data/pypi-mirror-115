import torch
from torch import Tensor

from ..utils import norm, to_t


def orientation_rotation_matrix(orientation: Tensor) -> Tensor:
    return get_rotation_matrix_from_vectors_t(
        to_t([0, 0, 1], device=orientation.device, dtype=orientation.dtype),
        orientation
    )


@torch.jit.script
def quaternion_to_matrix(quaternions: Tensor):
    """
    Convert rotations given as quaternions to rotation matrices.
    Args:
        quaternions: quaternions with real part first,
            as tensor of shape (..., 4).
    Returns:
        Rotation matrices as tensor of shape (..., 3, 3).
    """
    r, i, j, k = torch.unbind(quaternions, -1)
    two_s = 2.0 / (quaternions * quaternions).sum(-1)

    o = torch.stack(
        (
            1 - two_s * (j * j + k * k),
            two_s * (i * j - k * r),
            two_s * (i * k + j * r),
            two_s * (i * j + k * r),
            1 - two_s * (i * i + k * k),
            two_s * (j * k - i * r),
            two_s * (i * k - j * r),
            two_s * (j * k + i * r),
            1 - two_s * (i * i + j * j),
        ),
        -1,
    )
    return o.reshape(quaternions.shape[:-1] + (3, 3))


@torch.jit.script
def get_rotation_matrix_from_vectors_t(v1: Tensor, v2: Tensor):
    v1, v2 = norm(v1), norm(v2)
    axis = norm(torch.cross(v1, v2))
    angle = torch.arccos(torch.dot(v1, v2)) / 2
    quaternion = torch.cat([
        torch.cos(angle)[None],
        torch.sin(angle) * axis,
    ])
    return quaternion_to_matrix(quaternion)
