import enum


class TenderServiceTypeEnum(str, enum.Enum):
    CONSTRUCTION = "Construction"
    DELIVERY = "Delivery" 
    MANUFACTURE = "Manufacture"


class TenderStatusEnum(str, enum.Enum):
    CREATED = "Created"
    PUBLISHED = "Published"
    CLOSED = "Closed"

