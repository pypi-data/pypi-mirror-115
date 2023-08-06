from pathlib import Path
from crystals import Crystal

import numpy as np
import torch
import pytest

CIF_DIR = Path(__file__).parent / 'data' / 'cifs'
CRYSTALS = [Crystal.from_cif(cif) for cif in CIF_DIR.rglob('*.cif')]
CRYSTAL_NAMES = [Path(crystal.source).stem + ' ' + crystal.lattice_system.name for crystal in CRYSTALS]
ORIENTATIONS = ((0, 0, 1), (5, -13, 3), (1, 0, 0), (-1, -2, -3))


@pytest.fixture
def np_rng():
    return np.random.default_rng(seed=42)


@pytest.fixture(params=CRYSTALS, ids=CRYSTAL_NAMES)
def crystal(request):
    return request.param


@pytest.fixture
def device():
    return 'cuda' if torch.cuda.is_available() else 'cpu'


@pytest.fixture(
    params=ORIENTATIONS,
    ids=[str(o) for o in ORIENTATIONS],
)
def orientation(request):
    return request.param


@pytest.fixture
def q_vectors(np_rng):
    return np_rng.uniform(0.01, 10, (15, ))
