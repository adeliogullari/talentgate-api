from enum import Enum


class UserSubscriptionPlan(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"


class UserSubscriptionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"


class UserRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
