from itertools import product
from periodictable import cromermann as cr_ff
from crystals import Crystal
import numpy as np
from scipy.spatial.transform import Rotation

from collections import defaultdict


def get_cmf(symbol, charge=None):
    """
    Calculate x-ray scattering factors at specified sin(theta)/lambda

    *symbol* : string
        symbol of an element or ion, e.g., "Ca", "Ca2+"
    *charge* : int
        ion charge, overrides any valence suffixes such as "-", "+", "3+".

    Return float or numpy.array.
    """
    # resolve lookup symbol smbl, by default symbol
    smbl = symbol
    # build standard element or ion symbol
    if charge is not None:
        smbl = symbol.rstrip('012345678+-')
        if charge:
            smbl += ("%+i" % charge)[::-1]
    # convert Na+ or Cl- to Na1+, Cl1-
    elif symbol[-1:] in '+-' and not symbol[-2:-1].isdigit():
        smbl = (symbol[:-1] + "1" + symbol[-1:])
    # smbl is resolved here
    cmf = cr_ff.getCMformula(smbl)
    return CromerMannFormula(cmf.symbol, cmf.a, cmf.b, cmf.c)


class CromerMannFormula(object):
    """
    Cromer-Mann formula for x-ray scattering factors.
    Coefficient storage and evaluation.
    Class data:
    *stollimit* : float | |1/Ang|
        maximum sin(theta)/lambda for which the formula works
    Attributes:
    *symbol* : string
        symbol of an element
    *a* : [float]
        a-coefficients
    *b* : [float]
        b-coefficients
    *c* : float
        c-coefficient
    """

    # obtained from tables/f0_WaasKirf.dat and the associated reference
    # D. Waasmaier, A. Kirfel, Acta Cryst. (1995). A51, 416-413
    # http://dx.doi.org/10.1107/S0108767394013292
    stollimit = 6

    def __init__(self, symbol, a, b, c):
        """
        Create a new instance of CromerMannFormula for specified element.
        No return value
        """
        self.symbol = symbol
        self.a = np.asarray(a, dtype=float)
        self.a_diag = np.diag(a)
        self.b = np.asarray(b, dtype=float)[..., None]
        self.c = float(c)

    def __repr__(self):
        return f'CromerMannFormula({self.symbol})'

    def get_ff(self, q):
        return get_ff(q, self.a_diag, self.b, self.c)


def get_ff(q, adiag, b, c):
    stolflat = np.asarray(q / 4 / np.pi)
    bstol2 = np.dot(b, (stolflat ** 2)[None])
    rvrows = np.dot(adiag, np.exp(-bstol2))

    return rvrows.sum(axis=0) + c


def get_peaks(crystal: Crystal, orientation_vec: tuple, idx_min: int, idx_max: int):
    miller_indices = get_miller_indices(idx_min, idx_max)

    return get_peaks_from_indices(crystal, orientation_vec, miller_indices), miller_indices


def get_peaks_from_indices(crystal: Crystal, orientation_vec, miller_indices):
    mtx = get_crystal_mtx(crystal, orientation_vec)
    q_vectors = miller_indices @ mtx

    return q_vectors


def get_peaks_with_intensities(crystal, orientation_vec, idx_min, idx_max):
    miller_indices = get_miller_indices(idx_min, idx_max)
    coords, intensities = get_peaks_with_intensities_from_indices(crystal, orientation_vec, miller_indices)
    return coords, intensities, miller_indices


def get_peaks_with_intensities_from_indices(crystal, orientation_vec, miller_indices):
    q_vectors = get_peaks_from_indices(crystal, orientation_vec, miller_indices)
    cmf_dict = get_cmf_dict(crystal)
    atom_dict = get_coords_atom_dict(crystal)

    intensities = get_peak_intensities(miller_indices, q_vectors, atom_dict, cmf_dict)
    coords = get_2d_vector(q_vectors)

    return coords, intensities


def get_cmf_dict(crystal: Crystal) -> dict:
    elements = set(atom.element for atom in crystal)
    return {el: get_cmf(el) for el in elements}


def get_coords_atom_dict(crystal: Crystal):
    atom_dict = defaultdict(list)

    for atom in crystal:
        atom_dict[atom.element].append(atom.coords_fractional)
    for k, v in atom_dict.items():
        atom_dict[k] = np.array(v)
    return atom_dict


def get_rotation_matrix_from_vectors(v1: tuple, v2: tuple):
    v1, v2 = np.asarray(v1), np.asarray(v2)
    v1, v2 = norm(v1), norm(v2)

    v_cross = np.cross(v1, v2)
    v_cross = norm(v_cross)
    angle = np.arccos(np.dot(v1, v2))

    return Rotation.from_rotvec(v_cross * angle).as_matrix()


def get_2d_vector(vec: np.ndarray):
    return np.stack([
        np.sqrt(np.sum(vec[..., :2] ** 2, axis=-1)),
        np.asarray(vec[..., 2])
    ], axis=-1)


def get_vector_len(vec):
    return np.sqrt(np.sum(vec ** 2, axis=-1))


def get_crystal_mtx(crystal, orientation_vec=None):
    reciprocal_vectors = np.array(crystal.reciprocal_vectors)
    if orientation_vec and tuple(orientation_vec) != (0, 0, 1):
        rot_mtx = get_rotation_matrix_from_vectors((0, 0, 1), orientation_vec)
        return (rot_mtx @ reciprocal_vectors.T).T
    return reciprocal_vectors


def get_peak_intensities(miller_indices, q_vectors, atom_dict, cmf_dict):
    sfs = 0

    for el, coords in atom_dict.items():
        sfs += get_sf(cmf_dict[el], coords, get_vector_len(q_vectors), miller_indices)

    return np.abs(sfs) ** 2


def get_sf(cmf: CromerMannFormula,
           coords: np.ndarray,
           q_vectors: np.ndarray,
           miller_indices: np.ndarray) -> np.ndarray:
    ffs = cmf.get_ff(q_vectors)
    sf = ffs[..., None] * np.exp(2 * np.pi * 1j * np.einsum('ji,ki->jk', miller_indices, coords))
    return sf.sum(-1)


def get_miller_indices(idx_min: int, idx_max: int):
    return np.array(_get_all_combinations(idx_min, idx_max))


def _get_all_combinations(idx_min: int, idx_max: int):
    return list(filter(
        lambda x: any(x) != 0,
        product(list(range(idx_min, idx_max + 1)), repeat=3)
    ))


def length(t: np.ndarray):
    return np.linalg.norm(np.asarray(t))


def norm(t: np.ndarray):
    t_length = length(t)
    if t_length > 0:
        return t / t_length
    return t
