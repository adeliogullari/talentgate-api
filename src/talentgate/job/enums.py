from enum import StrEnum


class JobEmploymentType(StrEnum):
    INTERNSHIP = "internship"
    CONTRACTOR = "contractor"
    PART_TIME = "part-time"
    FULL_TIME = "full-time"


class JobLocationType(StrEnum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ON_SITE = "on-site"


class JobSalaryFrequency(StrEnum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
