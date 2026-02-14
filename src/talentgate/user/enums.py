from enum import StrEnum


class UserSubscriptionPlan(StrEnum):
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"


class UserSubscriptionStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"


class UserRole(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
