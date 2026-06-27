from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.models.role import Permission, Role, UserRole
from app.models.user import User
from app.schemas.role import AssignRoleRequest, RoleCreate, RoleResponse, RoleUpdate

router = APIRouter()


@router.get("/", response_model=list[RoleResponse])
def list_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return (
        db.query(Role)
        .filter(Role.company_id == current_user.company_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    permission_ids = role_in.permission_ids
    role = Role(
        company_id=role_in.company_id,
        name=role_in.name,
        description=role_in.description,
        is_active=role_in.is_active,
    )
    if permission_ids:
        role.permissions = (
            db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: UUID,
    role_in: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    update_data = role_in.model_dump(exclude_unset=True)
    permission_ids = update_data.pop("permission_ids", None)

    for field, value in update_data.items():
        setattr(role, field, value)

    if permission_ids is not None:
        role.permissions = (
            db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        )

    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="System roles cannot be deleted",
        )
    db.delete(role)
    db.commit()
    return None


@router.post("/assign", status_code=status.HTTP_204_NO_CONTENT)
def assign_role(
    assignment: AssignRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    existing = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == assignment.user_id,
            UserRole.role_id == assignment.role_id,
            UserRole.branch_id == assignment.branch_id,
        )
        .first()
    )
    if existing:
        return None

    user_role = UserRole(
        user_id=assignment.user_id,
        role_id=assignment.role_id,
        branch_id=assignment.branch_id,
    )
    db.add(user_role)
    db.commit()
    return None


@router.post("/unassign", status_code=status.HTTP_204_NO_CONTENT)
def unassign_role(
    assignment: AssignRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    db.query(UserRole).filter(
        UserRole.user_id == assignment.user_id,
        UserRole.role_id == assignment.role_id,
        UserRole.branch_id == assignment.branch_id,
    ).delete()
    db.commit()
    return None
