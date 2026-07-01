from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.session import UserSession
from app.security.hashing import verify_password
from app.security.jwt import create_access_token, create_refresh_token, decode_refresh_token
from app.schemas.token import Token

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    # البحث عن المستخدم بواسطة اسم المستخدم
    user = db.query(User).filter(User.username == form_data.username, User.is_deleted == False).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    # تسجيل الجلسة في قاعدة البيانات
    expire_at = datetime.now(timezone.utc) + timedelta(days=30)
    db_session = UserSession(
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=expire_at
    )
    db.add(db_session)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=Token)
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
) -> Any:
    try:
        payload = decode_refresh_token(refresh_token)
        user_id = payload.sub
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    
    # التحقق من وجود الجلسة وصلاحيتها داخل قاعدة البيانات
    db_session = db.query(UserSession).filter(
        UserSession.refresh_token == refresh_token,
        UserSession.user_id == user_id,
        UserSession.expires_at > datetime.now(timezone.utc)
    ).first()
    
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired refresh token session"
        )
        
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive or not found"
        )
        
    new_access_token = create_access_token(subject=user.id)
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
