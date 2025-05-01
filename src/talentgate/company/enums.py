from enum import Enum


class CompanyLocationType(str, Enum):
    HEADQUARTERS = "Headquarters"
    OFFICE = "Office"


class LinkType(str, Enum):
    WEBSITE = "Website"
    LINKEDIN = "LinkedIn"
    GITHUB = "Github"
