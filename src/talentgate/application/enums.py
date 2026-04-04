from enum import StrEnum


class ApplicationStatus(StrEnum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    WITHDRAWN = "withdrawn"
