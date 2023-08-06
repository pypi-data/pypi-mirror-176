from typing import Optional
from fastapi_camelcase import CamelModel


class ReportAddress(CamelModel):
    location_id: str
    address: str
    best_match_address: str
    qual_status: Optional[str] = None
    carrier: Optional[str] = None
    best_offer: Optional[str] = None
    speed: Optional[str] = None
    technology: Optional[str] = None
    region_clli: Optional[str] = None
    nearest_distance: Optional[str] = None
    location_type: Optional[str] = None
    comments: Optional[str] = None


class ReportAddressUpdateDto(CamelModel):
    address: Optional[str]
    best_match_address: Optional[str]
    qual_status: Optional[str] = None
    carrier: Optional[str] = None
    best_offer: Optional[str] = None
    speed: Optional[str] = None
    technology: Optional[str] = None
    region_clli: Optional[str] = None
    nearest_distance: Optional[str] = None
    location_type: Optional[str] = None
    comments: Optional[str] = None
