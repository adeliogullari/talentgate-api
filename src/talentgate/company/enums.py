from enum import Enum


class CompanyLocationType(str, Enum):
    HEADQUARTERS = "Headquarters"
    OFFICE = "Office"


class CompanyLinkType(str, Enum):
    WEBSITE = "Website"
    LINKEDIN = "LinkedIn"
    GITHUB = "Github"


class CompanyInvitationStatus(str, Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"


class CompanyEmployeeTitle(str, Enum):
    FOUNDER = "Founder"
    RECRUITER = "Recruiter"
