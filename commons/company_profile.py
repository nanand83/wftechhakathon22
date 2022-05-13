from py_dto import DTO
from teammember import TeamMember
class CompanyProfile(DTO):
    name: str
    website: str
    address: str
    team : list[TeamMember]