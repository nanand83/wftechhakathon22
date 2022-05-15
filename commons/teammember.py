from py_dto import DTO
from typing import Optional

class TeamMember(DTO):
    name: Optional[str]
    role: Optional[str]
    gender: Optional[str]
    ethnic: Optional[str]
