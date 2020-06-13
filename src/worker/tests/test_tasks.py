from dataclasses import dataclass

from app import tasks


def test_run_synspec(monkeypatch):
    test_args = dict(teff=20000, logg=4, wstart=4400, wend=4401)
    test_spectrum = [
        {"wavelength": 4400, "flux": 35080000},
        {"wavelength": 4400.01, "flux": 35070000},
    ]

    @dataclass
    class SynspecWrapperMocker:
        teff: float
        logg: float
        wstart: float
        wend: float
        relative: bool = False

        def calculate_spectrum(self):
            self.spectrum = test_spectrum

    monkeypatch.setattr(tasks, "SynspecWrapper", SynspecWrapperMocker)
    returned_spectrum = tasks.run_synspec(**test_args)

    assert returned_spectrum == test_spectrum  # nosec
