from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.resource import Resource as ResourceModel
from app.schemas.resource import Resource, ResourceCreate
from app.services.auth import get_current_user, require_ceo
from app.models.user import User as UserModel

router = APIRouter(
    prefix="/resources",
    tags=["resources"]
)

@router.get("/", response_model=List[Resource])
def read_resources(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    resources = db.query(ResourceModel).all()
    return resources

@router.get("/project/{record_id}", response_model=List[Resource])
def read_resources_by_project(record_id: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    resources = db.query(ResourceModel).filter(ResourceModel.assigned_record_id == record_id).all()
    return resources

@router.post("/", response_model=Resource)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(require_ceo)):
    db_resource = ResourceModel(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource
