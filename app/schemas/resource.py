from pydantic import BaseModel
from typing import Optional

class ResourceBase(BaseModel):
    resource_name: str
    role: Optional[str] = None
    email: Optional[str] = None
    access_level: Optional[str] = "READ"
    assigned_record_id: Optional[str] = None

class ResourceCreate(ResourceBase):
    pass

class Resource(ResourceBase):
    id: int

    class Config:
        from_attributes = True
