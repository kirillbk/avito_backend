import enum


class BidStatusEnum(str, enum.Enum):
    CREATED = "Created"
    PUBLISHED = "Published"
    CANCELED = "Canceled"


class BidAuthorTypeEnum(str, enum.Enum):
    ORGANIZATION = "Organization"
    USER = "User"