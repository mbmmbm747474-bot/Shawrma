from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.security.hashing import hash_password

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    users = (
        db.query(User)
        .filter(User.is_deleted == False, User.company_id == current_user.company_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return users


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> Any:
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    existing = (
        db.query(User)
        .filter((User.username == user_in.username) | (User.email == user_in.email))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username or email already exists",
        )

    user = User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        mobile=user_in.mobile,
        language=user_in.language,
        timezone=user_in.timezone,
        avatar=user_in.avatar,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
        password_hash=hash_password(user_in.password),
        company_id=user_in.company_id,
        branch_id=user_in.branch_id,
        created_by=current_user.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        password = update_data.pop("password")
        if password:
            user.password_hash = hash_password(password)

    for field, value in update_data.items():
        setattr(user, field, value)
    user.updated_by = current_user.id

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    from datetime import datetime, timezone

    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_deleted = True
    user.deleted_at = datetime.now(timezone.utc)
    user.deleted_by = current_user.id
    user.is_active = False
    db.add(user)
    db.commit()
    return None
