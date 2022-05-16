from py_dto import DTO
from typing import Optional

class TeamMember(DTO):
    name: Optional[str]
    gender: Optional[str]
    ethnicity: Optional[str]
