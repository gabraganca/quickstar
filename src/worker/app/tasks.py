from typing import List, Dict

from app.synspec.wrapper import SynspecWrapper
from app.celery import celery_app


@celery_app.task(acks_late=True)
def run_synspec(
    teff: float, logg: float, wstart: float, wend: float, relative: bool = False,
) -> List[Dict[str, float]]:

    syn = SynspecWrapper(
        teff=teff, logg=logg, wstart=wstart, wend=wend, relative=relative
    )
    syn.calculate_spectrum()
    return syn.spectrum
