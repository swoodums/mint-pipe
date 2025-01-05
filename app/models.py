from pydantic import BaseModel, Field
from typing import List, Literal, Annotated
from fastapi import Query
from enum import Enum

class TwoLineElementRecord(BaseModel):
    """
    A single Two-Line Element record
    
    Contains information from a single record from the member list
    Notably, the encoded information in line1 and line2
    Reference https://ensatellite.com/tle/ for details.
    """
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    satelliteId: int
    name: str
    date: str
    line1: str
    line2: str

# Creates a class that holds the payload from the source.
class SourcePayload(BaseModel):
    """
    The response payload from the source API.
    """
    context: str = Field(alias="@context")
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    totalItems: int
    member: List[TwoLineElementRecord]
    parameters: dict
    view: dict

# Creates a class that holds the transformed TLE
class TwoLineElementRecordParsed(BaseModel):
    """
    A single parsed Two-Line Element record
    
    Contains information from a single record from the member list that has been
    parsed.  The Two-Line Element has been decoded and represented as key-value
    pairs. Reference https://ensatellite.com/tle/ for details.
    """
    id: str
    type: str
    satelliteId: int
    name: str
    date: str
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

# Creates a class that holds the payload after the TLE records have been parsed.
class ModifiedPayload(BaseModel):
    """
    The modified response payload from the source API.
    """
    context: str
    id: str
    type: str
    totalItems: int
    member: List[TwoLineElementRecordParsed]
    parameters: dict
    view: dict

class SortEnum(str, Enum):
    id = 'id'
    name = 'name'
    popularity = 'popularity'
    inclination = 'inclination'
    eccentricity = 'eccentricity'
    period = 'period'

class SortDirEnum(str, Enum):
    asc = 'asc'
    desc = 'desc'

class QueryParams(BaseModel):
    """
    The query parameters for the tle api.
    """
    search: str | None = None
    sort: Literal["id", "name", "popularity", "inclination", "eccentricity", "period"] = None
    sort_dir: Literal["asc", "desc"] = None
    page: int = Field(ge=1)
    page: Annotated[int | None, Query(ge=1)] = None
    page_size: Annotated[int | None, Query(ge=1, lt=100)] = None