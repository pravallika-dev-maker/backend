from fastapi import Header, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User as UserModel

def get_current_user(x_user_email: str = Header(None), db: Session = Depends(get_db)):
    if not x_user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User email header missing"
        )
    
    user = db.query(UserModel).filter(UserModel.email == x_user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. User not authorized."
        )
    
    return user

def require_ceo(user: UserModel = Depends(get_current_user)):
    if not user.can_add_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. Only CEO/Admin can perform this action."
        )
    return user
