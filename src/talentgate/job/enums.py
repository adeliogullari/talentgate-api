from enum import Enum


class JobEmploymentType(str, Enum):
    INTERNSHIP = "internship"
    CONTRACTOR = "contractor"
    PART_TIME = "part-time"
    FULL_TIME = "full-time"


class JobLocationType(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ON_SITE = "on-site"


class JobSalaryFrequency(str, Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
