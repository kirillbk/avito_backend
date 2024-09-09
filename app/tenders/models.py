import enum


class tenderServiceTypeEnum(str, enum.Enum):
    CONSTRUCTION = "Construction"
    DELIVERY = "Delivery" 
    MANUFACTURE = "Manufacture"


class tenderStatusEnum(str, enum.Enum):
    CREATED = "Created"
    PUBLISHED = "Published"
    CLOSED = "Closed"

