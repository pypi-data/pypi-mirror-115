import numpy as np
from crystals import Crystal

import torch

from torch_crystals import numpy_simulations as np_sim
from torch_crystals import simulations as sim
from torch_crystals import to_np, to_t, length


def test_torch_vs_numpy(crystal: Crystal, device, orientation):
    coords, intensities, miller_indices = np_sim.get_peaks_with_intensities(crystal, orientation, -3, 3)
    torch_crystal = sim.TorchCrystal(crystal, device, orientation)
    q_xy, q_z = torch_crystal.get_q_vectors(to_t(miller_indices, device=device), mode='q_space')
    res_coords = np.stack([to_np(q_xy), to_np(q_z)], -1)
    assert np.allclose(res_coords, coords, atol=1e-5)
    q_vectors = length(torch.stack([q_xy, q_z], -1))
    sim_intensities = torch_crystal.intensity_calc(q_vectors, to_t(miller_indices, device=device))
    assert np.allclose(intensities, to_np(sim_intensities), atol=1e-5)


def test_miller_indices(device):
    miller_indices = sim.get_miller_indices(-3, 3, device=device)
    miller_indices_np = np_sim.get_miller_indices(-3, 3)
    assert np.allclose(to_np(miller_indices), miller_indices_np)


def test_atom_dicts(crystal: Crystal, device):
    atom_dict = sim.get_coords_atom_dict(crystal, device)
    np_atom_dict = np_sim.get_coords_atom_dict(crystal)

    for el, arr in np_atom_dict.items():
        assert el in atom_dict
        assert np.allclose(to_np(atom_dict[el]), arr)


def test_cmf_dict(crystal: Crystal, device, q_vectors):
    np_cmf_dict = np_sim.get_cmf_dict(crystal)
    cmf_dict = sim.get_cmf_dict(crystal, device)

    for el, np_cmf in np_cmf_dict.items():
        assert el in cmf_dict
        cmf = cmf_dict[el]

        assert np.allclose(to_np(cmf.a_diag), np_cmf.a_diag)
        assert np.allclose(to_np(cmf.b), np_cmf.b)
        assert cmf.c == np_cmf.c

        ff = cmf.get_ff(q_vectors)
        np_ff = np_cmf.get_ff(q_vectors)
        assert np.allclose(to_np(ff), np_ff)


def test_get_sf(crystal: Crystal, device):
    miller_indices = np_sim.get_miller_indices(-3, 3)
    np_cmf_dict = np_sim.get_cmf_dict(crystal)
    cmf_dict = sim.get_cmf_dict(crystal, device)
    peaks = np_sim.get_peaks_from_indices(crystal, (0, 0, 1), miller_indices)
    q_vectors = np.sqrt((peaks ** 2).sum(-1))

    atom_dict = sim.get_coords_atom_dict(crystal, device)

    for el, coords in atom_dict.items():
        np_sf = np_sim.get_sf(np_cmf_dict[el], to_np(coords), q_vectors, miller_indices)
        sf = sim.get_sf(cmf_dict[el], coords, to_t(q_vectors), to_t(miller_indices))
        for s, ns in zip(to_np(sf), np_sf):
            assert np.abs(s - ns) < 1e-6
