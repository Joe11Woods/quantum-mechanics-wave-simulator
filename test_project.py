from project import get_L, get_time_period, rip
import numpy as np
import pytest
#Useful constants
HBAR = 1.054571817e-34



def test_get_L(monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _: "2")
    assert get_L() == 2

    inputs = iter(["-1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert get_L() == 2

    inputs = iter(["hello", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert get_L() == 2



def test_get_time_period():

    Psi = 1
    E = {1:1}
    assert get_time_period(Psi,E) == 2* np.pi * HBAR

    E = {1:1,
         2:2}
    assert get_time_period(Psi,E) == 2 * np.pi * HBAR


def test_rip():

    psi = {1:1}
    E = {1:1}

    assert rip(psi,E) == (1+0j,1.0,0.0,1.0)

    psi = {2:1}

    with pytest.raises(KeyError):
        rip(psi, E)




