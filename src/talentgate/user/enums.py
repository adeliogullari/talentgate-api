from enum import Enum


class SubscriptionPlan(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"


class UserRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
