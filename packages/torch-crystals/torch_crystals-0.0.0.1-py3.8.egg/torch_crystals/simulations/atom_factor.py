from math import pi

import torch
from torch import Tensor
from torch import tensor

from periodictable import cromermann as cr_ff


def get_cmf(symbol, charge=None, device: torch.device = 'cuda', dtype: torch.dtype = torch.float64):
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
    return CromerMannFormula(cmf.symbol, cmf.a, cmf.b, cmf.c, device, dtype)


class CromerMannFormula(object):
    """
    Cromer-Mann formula for x-ray scattering factors.
    Coefficient storage and evaluation.
    """

    # obtained from tables/f0_WaasKirf.dat and the associated reference
    # D. Waasmaier, A. Kirfel, Acta Cryst. (1995). A51, 416-413
    # http://dx.doi.org/10.1107/S0108767394013292
    stollimit = 6

    def __init__(self, symbol, a, b, c, device: torch.device, dtype: torch.dtype = torch.float64):
        """
        Create a new instance of CromerMannFormula for specified element.
        No return value
        """
        self.dtype = dtype
        self.device = device
        self.symbol = symbol
        self.a = tensor(a, dtype=self.dtype, device=self.device)
        self.a_diag = torch.diag(self.a)
        self.b = tensor(b, dtype=self.dtype, device=self.device)[:, None]
        self.c = float(c)

    def __repr__(self):
        return f'CromerMannFormula({self.symbol})'

    def get_ff(self, q: Tensor):
        return get_ff(torch.as_tensor(q).to(self.dtype).to(self.device), self.a_diag, self.b, self.c)


def get_ff(q: Tensor, adiag: Tensor, b: Tensor, c: float) -> Tensor:
    stolflat = ((q / 4 / pi) ** 2)[None]
    bstol2 = torch.einsum('ij,jk->ik', b, stolflat)
    rvrows = torch.einsum('ij,jk->ik', adiag, torch.exp(-bstol2))

    return rvrows.sum(0) + c
