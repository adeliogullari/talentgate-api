from enum import StrEnum


class ApplicationStatus(StrEnum):
    APPLIED = "Applied"
    SCREENING = "Screening"
    REFERENCE_CHECK = "Reference Check"
    OFFER = "Offer"
    WITHDRAWN = "Withdrawn"
