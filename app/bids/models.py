import enum


class bidStatusEnum(str, enum.Enum):
    CREATED = "Created"
    PUBLISHED = "Published"
    CANCELED = "Canceled"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class authorTypeEnum(str, enum.Enum):
    ORGANIZATION = "Organization"
    USER = "User"