from pydantic import BaseModel, Field
from typing import List

class TwoLineElementRecord(BaseModel):
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    satelliteId: int
    name: str
    date: str
    line1: str
    line2: str

class TwoLineElementRecordParsed(BaseModel):
    id: str
    type: str
    satelliteId: int
    name: str
    date: str
    line_number: int
    satellite_catalog_number: int
    classification: str
    international_designator: str
    epoch_year: int
    epoch_day: float
    first_derivative_mean_motion: float
    second_derivative_mean_motion: float
    bstar: float
    ephemeris_type: int
    element_set_number: int
    line1_check_sum: int
    inclination: float
    right_ascension: float
    eccentricity: float
    argument_of_perigee: float
    mean_anomaly: float
    mean_motion: float
    revolution_number: int
    line2_check_sum: int

class SourcePayload(BaseModel):
    context: str = Field(alias="@context")
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    totalItems: int
    member: List[TwoLineElementRecord]
    parameters: dict
    view: dict

class ModifiedPayload(BaseModel):
    context: str
    id: str
    type: str
    totalItems: int
    member: List[TwoLineElementRecordParsed]
    parameters: dict
    view: dict