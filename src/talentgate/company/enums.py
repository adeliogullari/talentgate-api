from enum import StrEnum


class CompanyLocationType(StrEnum):
    HEADQUARTERS = "Headquarters"
    OFFICE = "Office"


class CompanyLinkType(StrEnum):
    WEBSITE = "Website"
    LINKEDIN = "LinkedIn"
    GITHUB = "Github"


class CompanyInvitationStatus(StrEnum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"


class CompanyEmployeeTitle(StrEnum):
    FOUNDER = "Founder"
    RECRUITER = "Recruiter"
