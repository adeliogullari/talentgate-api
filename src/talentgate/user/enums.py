from enum import Enum


class SubscriptionPlan(str, Enum):
    BASIC = "Basic"
    STANDARD = "Standard"


class SubscriptionStatus(str, Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"


class UserRole(str, Enum):
    OWNER = "Owner"
    ADMIN = "Admin"
