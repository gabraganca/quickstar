from typing import List, Dict
import os
import csv
import subprocess

from app.settings import SYNSPEC_PATH


class NoSpectrumError(Exception):
    pass


class SynspecWrapper:
    def __init__(
        self,
        teff: float,
        logg: float,
        wstart: float,
        wend: float,
        relative: bool = False,
    ):

        self.parameters = {
            "teff": teff,
            "logg": logg,
            "wstart": wstart,
            "wend": wend,
            "relative": relative,
            "noplot": "1",
        }

        self.spath = SYNSPEC_PATH
        self._remove_spectrum()

    @property
    def synplot_cmd(self):

        synplot_args = [
            key + " = " + str(value) for key, value in self.parameters.items()
        ]

        cmd = "CD, '" + self.spath + "' & synplot, " + ", ".join(synplot_args)

        return 'gdl -e "' + cmd + '"'

    def _remove_spectrum(self):
        try:
            os.remove(os.path.join(self.spath, "fort.11"))
        except OSError:
            pass

    @property
    def spectrum(self) -> List[Dict[str, float]]:
        try:
            with open(os.path.join(self.spath, "fort.11")) as f:
                reader = csv.DictReader(
                    f,
                    delimiter=" ",
                    skipinitialspace=True,
                    fieldnames=("wavelength", "flux"),
                )
                return [{k: float(v) for k, v in row.items()} for row in reader]
        except FileNotFoundError:
            raise NoSpectrumError(
                "Calculated spectrum is not available. Check if syn(spec|plot) ran correctly."
            )

    def calculate_spectrum(self):

        self._remove_spectrum()
        subprocess.call(self.synplot_cmd, shell=True)
