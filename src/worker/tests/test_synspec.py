import os
import subprocess

import pytest

from app.synspec import wrapper


def test_synspecwrapper_remove_spectrum(mocker):
    syn = wrapper.SynspecWrapper(teff=20000, logg=4, wstart=4400, wend=4600)

    mocker.patch("os.remove")

    syn._remove_spectrum()

    os.remove.assert_called_once()


def test_synspecwrapper_no_spectrum():
    syn = wrapper.SynspecWrapper(teff=20000, logg=4, wstart=4400, wend=4401)

    with pytest.raises(wrapper.NoSpectrumError):
        syn.spectrum


def test_synspecwrapper_spectrum(mocker):
    syn = wrapper.SynspecWrapper(teff=20000, logg=4, wstart=4400, wend=4401)

    mock_spectrum_file = "  4400.000 3.508E+07\n  4400.010 3.507E+07\n"
    test_spectrum = [
        {"wavelength": 4400, "flux": 35080000},
        {"wavelength": 4400.01, "flux": 35070000},
    ]

    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_spectrum_file))
    returned_spectrum = syn.spectrum

    assert returned_spectrum == test_spectrum  # nosec


def test_synspecwrapper_calculate_spectrum(mocker):
    syn = wrapper.SynspecWrapper(teff=20000, logg=4, wstart=4400, wend=4401)

    mocker.patch("subprocess.call")
    syn.calculate_spectrum()

    subprocess.call.assert_called_once()
