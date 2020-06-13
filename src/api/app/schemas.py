from typing import List, Dict, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, PositiveFloat, PositiveInt


class SynspecParameters(BaseModel):
    teff: PositiveFloat
    logg: PositiveFloat
    wstart: PositiveFloat
    wend: PositiveFloat
    relative: bool = False

    class Config:
        schema_extra = {
            "example": {
                "teff": 20000.0,
                "logg": 4.0,
                "wstart": 4400,
                "wend": 4600,
                "relative": False,
            }
        }


class TaskBase(BaseModel):
    id: UUID


class TaskResult(TaskBase):
    status: str
    results: Optional[List[Dict[str, float]]]
    finished_at: Optional[datetime]
    total_count: Optional[PositiveInt]

    class Config:
        schema_extra = {
            "example": {
                "id": "22badc42-92f2-476c-8de9-57a3207b9956",
                "status": "SUCCESS",
                "results": [
                    {"wavelength": 4400, "flux": 35080000},
                    {"wavelength": 4400.01, "flux": 35070000},
                    {"wavelength": 4400.02, "flux": 35050000},
                ],
                "finished_at": "2020-05-23T02:11:08.338810",
                "total_count": 3,
            }
        }


class Health(BaseModel):
    status: bool
