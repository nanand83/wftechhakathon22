from py_dto import DTO
from teammember import TeamMember
from typing import Optional


class CompanyProfile(DTO):
    dunsNum: str
    name: str
    website: str
    address: Optional[str]
    team : list[dict]
    certifications: list[str]
    status: str
    lastUpdated: Optional[str]
