from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User as UserModel
from backend.app.schemas.user import User, UserCreate, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already authorized")
    
    # We no longer require passwords here for Magic Link flow
    new_user = UserModel(
        email=user.email,
        full_name=user.full_name,
        hashed_password=None,
        can_add_users=user.can_add_users if user.can_add_users is not None else False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/check-email/{email}")
def check_email(email: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Access not granted. Please contact the administrator."
        )
    return {"status": "authorized", "user": {"email": user.email, "full_name": user.full_name, "can_add_users": user.can_add_users}}

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access not granted. Please contact the administrator.",
        )
    
    # REQUIRE PASSWORD FOR CEO
    if user.can_add_users:
        if not user_data.password:
            raise HTTPException(status_code=400, detail="Password is required for CEO account")
        if user.hashed_password != user_data.password:
            raise HTTPException(status_code=401, detail="Incorrect password for CEO account")
            
    return {"message": "Access verified", "user": {"email": user.email, "full_name": user.full_name, "can_add_users": user.can_add_users}}
