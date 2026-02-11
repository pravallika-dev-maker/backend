from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.project import Project as ProjectModel
from app.models.stage import Stage as StageModel
from app.models.history import StageHistory as StageHistoryModel
from app.models.resource import Resource as ResourceModel
from app.schemas.project import Project, ProjectCreate, ProjectCreateRequest, ProjectUpdateRequest, ProjectStatusUpdate, ProjectStageSkipRequest
from app.services.auth import get_current_user, require_ceo
from app.models.user import User as UserModel
import uuid
from datetime import date

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@router.get("/", response_model=List[Project])
def read_projects(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Fetch projects with RBAC:
    - CEO sees ALL projects (including PRIVATE ones)
    - Regular users (READ/WRITE) see ONLY PUBLIC projects
    """
    query = db.query(ProjectModel)
    
    if not current_user.can_add_users:
        # Non-CEO users can only see public projects
        query = query.filter(ProjectModel.is_private == False)

    projects = query.offset(skip).limit(limit).all()
    return projects

@router.get("/{record_id}", response_model=Project)
def read_project(
    record_id: str, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_project = db.query(ProjectModel).filter(ProjectModel.record_id == record_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 🔐 Visibility Check:
    if not current_user.can_add_users:
        # Regular users cannot see private projects
        if db_project.is_private:
            raise HTTPException(status_code=403, detail="Access denied. This is a private project.")
            
    return db_project

@router.post("/", response_model=Project)
def create_project(
    project_data: ProjectCreateRequest, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Create a new project with automatic stage history initialization
    """
    # 🔐 Permission Check: CEO or WRITE access
    if not current_user.can_add_users and current_user.access_level != "WRITE":
        raise HTTPException(status_code=403, detail="Permission denied. You need WRITE access to create projects.")

    try:
        # Generate unique record ID
        record_id = f"P-{str(uuid.uuid4())[:8].upper()}"
        
        # Get the selected starting stage
        starting_stage = db.query(StageModel).filter(
            StageModel.stage_name == project_data.starting_stage_name
        ).first()
        
        if not starting_stage:
            raise HTTPException(status_code=400, detail=f"Starting stage '{project_data.starting_stage_name}' not found")
        
        # Determine next stage
        next_stage = db.query(StageModel).filter(
            StageModel.stage_order == starting_stage.stage_order + 1
        ).first()
        
        # Create the project
        db_project = ProjectModel(
            record_id=record_id,
            client_name=project_data.client_name,
            deal_type=project_data.deal_type,
            project_owner_name=project_data.project_owner_name,
            deal_value=project_data.deal_value,
            project_started_date=project_data.project_started_date,
            current_stage_name=starting_stage.stage_name,
            next_stage_name=next_stage.stage_name if next_stage else None,
            next_stage_expected_date=project_data.next_stage_expected_date,
            deal_status="Open",
            execution_status="Planning",
            is_private=project_data.is_private if current_user.can_add_users else False 
        )
        
        db.add(db_project)
        db.flush()  # Get the ID without committing
        
        # Initialize Stage History
        # 1. Mark all stages before starting stage as "Completed" with NULL dates
        # (We don't know actual dates for stages completed before project was added)
        completed_stages = db.query(StageModel).filter(
            StageModel.stage_order < starting_stage.stage_order
        ).all()
        
        for stage in completed_stages:
            history_entry = StageHistoryModel(
                record_id=record_id,
                stage_name=stage.stage_name,
                stage_start_date=None,  # Unknown - project added mid-lifecycle
                stage_end_date=None,     # Unknown - project added mid-lifecycle
                stage_status="Completed"
            )
            db.add(history_entry)
        
        # 2. Mark starting stage as "In Progress"
        current_history = StageHistoryModel(
            record_id=record_id,
            stage_name=starting_stage.stage_name,
            stage_start_date=project_data.project_started_date,
            stage_end_date=None,  # Still in progress
            stage_status="In Progress"
        )
        db.add(current_history)
        
        # 3. Handle Resources if provided
        if project_data.resources:
            for res_data in project_data.resources:
                db_resource = ResourceModel(
                    resource_name=res_data.resource_name,
                    role=res_data.role,
                    assigned_record_id=record_id
                )
                db.add(db_resource)
        
        db.commit()
        db.refresh(db_project)
        
        return db_project
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")

@router.patch("/{record_id}/status", response_model=Project)
def update_project_status(
    record_id: str, 
    status_data: ProjectStatusUpdate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Update project deal status and execution status
    """
    # Allowed values
    ALLOWED_DEAL_STATUS = ["Open", "Won", "Lost", "On Hold", "Closed"]
    ALLOWED_EXECUTION_STATUS = ["Planning", "In Progress", "On Hold", "Completed", "Cancelled"]
    
    # Validate status values
    if status_data.deal_status not in ALLOWED_DEAL_STATUS:
        raise HTTPException(status_code=400, detail=f"Invalid deal status. Allowed values: {', '.join(ALLOWED_DEAL_STATUS)}")
    
    if status_data.execution_status not in ALLOWED_EXECUTION_STATUS:
        raise HTTPException(status_code=400, detail=f"Invalid execution status. Allowed values: {', '.join(ALLOWED_EXECUTION_STATUS)}")
    
    # Get the project
    db_project = db.query(ProjectModel).filter(ProjectModel.record_id == record_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 🔐 Permission Check: CEO or WRITE access
    if not current_user.can_add_users:
        if current_user.access_level != "WRITE":
            raise HTTPException(status_code=403, detail="Permission denied. You need WRITE access to update projects.")
        if db_project.is_private:
            raise HTTPException(status_code=403, detail="Access denied. Regular users cannot modify private projects.")
    
    # Update status fields
    db_project.deal_status = status_data.deal_status
    db_project.execution_status = status_data.execution_status
    
    try:
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating project status: {str(e)}")

@router.post("/{record_id}/skip-to-stage", response_model=Project)
def skip_to_stage(
    record_id: str, 
    skip_data: ProjectStageSkipRequest, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Move or skip project to a selected stage
    """
    today = date.today().isoformat()
    
    # 1. Get the project
    db_project = db.query(ProjectModel).filter(ProjectModel.record_id == record_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # 🔐 Permission Check: CEO or WRITE access
    if not current_user.can_add_users:
        if current_user.access_level != "WRITE":
            raise HTTPException(status_code=403, detail="Permission denied. You need WRITE access to advance projects.")
        if db_project.is_private:
            raise HTTPException(status_code=403, detail="Access denied. Regular users cannot modify private projects.")
        
    # 2. Get current stage info
    current_stage = db.query(StageModel).filter(
        StageModel.stage_name == db_project.current_stage_name
    ).first()
    
    if not current_stage:
        raise HTTPException(status_code=500, detail="Current project stage not found in Stage_Master")
        
    # 3. Get selected stage info
    selected_stage = db.query(StageModel).filter(
        StageModel.stage_name == skip_data.selected_stage_name
    ).first()
    
    if not selected_stage:
        raise HTTPException(status_code=400, detail=f"Selected stage '{skip_data.selected_stage_name}' not found")
        
    # Validation: Stage order must always increase
    if selected_stage.stage_order <= current_stage.stage_order:
        raise HTTPException(status_code=400, detail="Cannot move backward or stay in the same stage")
        
    try:
        # 1. Close all currently open stages in Stage_History for this project
        open_histories = db.query(StageHistoryModel).filter(
            StageHistoryModel.record_id == record_id,
            StageHistoryModel.stage_end_date == None
        ).all()
        
        for hist in open_histories:
            hist.stage_end_date = today
            # If it was in progress, mark it as completed since we are moving to a new stage
            if hist.stage_status == "In Progress":
                hist.stage_status = "Completed"
            
        # 2. Handle intermediate stages (Skipped)
        skipped_stages = db.query(StageModel).filter(
            StageModel.stage_order > current_stage.stage_order,
            StageModel.stage_order < selected_stage.stage_order
        ).order_by(StageModel.stage_order).all()
        
        for stage in skipped_stages:
            skipped_history = StageHistoryModel(
                record_id=record_id,
                stage_name=stage.stage_name,
                stage_start_date=today,
                stage_end_date=today,
                stage_status="Skipped"
            )
            db.add(skipped_history)
            
        # 3. Insert selected stage into Stage_History
        new_history = StageHistoryModel(
            record_id=record_id,
            stage_name=selected_stage.stage_name,
            stage_start_date=today,
            stage_end_date=None,
            stage_status="In Progress"
        )
        db.add(new_history)
        
        # 4. Update Projects table
        db_project.current_stage_name = selected_stage.stage_name
        db_project.project_started_date = today # Update start date to current stage start date
        
        # Update next stage and expected date
        if skip_data.next_stage_expected_date:
            db_project.next_stage_expected_date = skip_data.next_stage_expected_date
            
        next_stage = db.query(StageModel).filter(
            StageModel.stage_order > selected_stage.stage_order
        ).order_by(StageModel.stage_order).first()
        
        db_project.next_stage_name = next_stage.stage_name if next_stage else None
        
        db.commit()
        db.refresh(db_project)
        return db_project
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error moving stage: {str(e)}")

@router.put("/{record_id}", response_model=Project)
def update_project(
    record_id: str, 
    project_data: ProjectUpdateRequest, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Update project details including resources
    """
    db_project = db.query(ProjectModel).filter(ProjectModel.record_id == record_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 🔐 Permission Check: CEO or WRITE access
    if not current_user.can_add_users:
        if current_user.access_level != "WRITE":
            raise HTTPException(status_code=403, detail="Permission denied. You need WRITE access to edit projects.")
        if db_project.is_private:
            raise HTTPException(status_code=403, detail="Access denied. Regular users cannot modify private projects.")
    
    # Update base fields if provided
    if project_data.client_name is not None:
        db_project.client_name = project_data.client_name
    if project_data.project_owner_name is not None:
        db_project.project_owner_name = project_data.project_owner_name
    if project_data.deal_value is not None:
        db_project.deal_value = project_data.deal_value
    if project_data.project_started_date is not None:
        db_project.project_started_date = project_data.project_started_date
    if project_data.next_stage_expected_date is not None:
        db_project.next_stage_expected_date = project_data.next_stage_expected_date
    
    # 🔐 Only CEO can change privacy status
    if project_data.is_private is not None and current_user.can_add_users:
        db_project.is_private = project_data.is_private
        
    try:
        # Handle Resources if provided
        if project_data.resources is not None:
            # Delete old resources
            db.query(ResourceModel).filter(ResourceModel.assigned_record_id == record_id).delete()
            
            # Add new resources
            for res_data in project_data.resources:
                db_resource = ResourceModel(
                    resource_name=res_data.resource_name,
                    role=res_data.role,
                    assigned_record_id=record_id
                )
                db.add(db_resource)
        
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating project: {str(e)}")

@router.delete("/{record_id}")
def delete_project(
    record_id: str, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Delete a project and its associated history/resources
    """
    db_project = db.query(ProjectModel).filter(ProjectModel.record_id == record_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 🔐 Permission Check: CEO or WRITE access
    if not current_user.can_add_users:
        if current_user.access_level != "WRITE":
            raise HTTPException(status_code=403, detail="Permission denied. You need WRITE access to delete projects.")
        if db_project.is_private:
            raise HTTPException(status_code=403, detail="Access denied. Regular users cannot modify private projects.")
    
    try:
        # Delete history
        db.query(StageHistoryModel).filter(StageHistoryModel.record_id == record_id).delete()
        
        # Delete resources
        db.query(ResourceModel).filter(ResourceModel.assigned_record_id == record_id).delete()
        
        # Delete project
        db.delete(db_project)
        
        db.commit()
        return {"message": "Project deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting project: {str(e)}")
