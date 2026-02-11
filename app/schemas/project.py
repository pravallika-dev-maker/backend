from pydantic import BaseModel
from typing import Optional, List

class ProjectBase(BaseModel):
    record_id: str
    client_name: Optional[str] = None
    deal_type: Optional[str] = None
    deal_value: Optional[float] = 0
    project_owner_name: Optional[str] = None
    current_stage_name: Optional[str] = None
    next_stage_name: Optional[str] = None
    next_stage_expected_date: Optional[str] = None
    deal_status: Optional[str] = None
    execution_status: Optional[str] = None
    project_started_date: Optional[str] = None
    is_private: Optional[bool] = False

class ResourceCreateSimple(BaseModel):
    """Schema for creating a resource within a project request"""
    resource_name: str
    role: Optional[str] = None

class ProjectCreateRequest(BaseModel):
    """Schema for creating a new project"""
    client_name: str
    deal_type: str  # "Pilot" or "Project"
    project_owner_name: str
    deal_value: float
    project_started_date: str
    starting_stage_name: str
    next_stage_expected_date: Optional[str] = None
    parent_record_id: Optional[str] = None
    is_private: Optional[bool] = False
    resources: Optional[List[ResourceCreateSimple]] = []

class ProjectUpdateRequest(BaseModel):
    """Schema for updating an existing project"""
    client_name: Optional[str] = None
    project_owner_name: Optional[str] = None
    deal_value: Optional[float] = None
    project_started_date: Optional[str] = None
    next_stage_expected_date: Optional[str] = None
    is_private: Optional[bool] = None
    resources: Optional[List[ResourceCreateSimple]] = None

class ProjectStatusUpdate(BaseModel):
    """Schema for updating project status fields"""
    deal_status: str
    execution_status: str

class ProjectStageSkipRequest(BaseModel):
    """Schema for skipping/moving to a new stage"""
    selected_stage_name: str
    next_stage_expected_date: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True
