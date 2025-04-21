from enum import Enum


class EmployeeTitle(str, Enum):
    FOUNDER = "Founder"
    RECRUITER = "Recruiter"
