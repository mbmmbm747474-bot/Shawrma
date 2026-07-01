from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.models.branch import Branch
from app.models.user import User
from app.schemas.branch import BranchCreate, BranchResponse, BranchUpdate

router = APIRouter()


@router.get("/", response_model=list[BranchResponse])
def list_branches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    company_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    query = db.query(Branch).filter(Branch.is_deleted == False)
    if company_id:
        query = query.filter(Branch.company_id == company_id)
    else:
        query = query.filter(Branch.company_id == current_user.company_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{branch_id}", response_model=BranchResponse)
def get_branch(
    branch_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    branch = (
        db.query(Branch)
        .filter(Branch.id == branch_id, Branch.is_deleted == False)
        .first()
    )
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    return branch


@router.post("/", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
def create_branch(
    branch_in: BranchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    branch = Branch(**branch_in.model_dump())
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch


@router.put("/{branch_id}", response_model=BranchResponse)
def update_branch(
    branch_id: UUID,
    branch_in: BranchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    branch = (
        db.query(Branch)
        .filter(Branch.id == branch_id, Branch.is_deleted == False)
        .first()
    )
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")

    for field, value in branch_in.model_dump(exclude_unset=True).items():
        setattr(branch, field, value)

    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch


@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(
    branch_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    from datetime import datetime, timezone

    branch = (
        db.query(Branch)
        .filter(Branch.id == branch_id, Branch.is_deleted == False)
        .first()
    )
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")

    branch.is_deleted = True
    branch.deleted_at = datetime.now(timezone.utc)
    branch.is_active = False
    db.add(branch)
    db.commit()
    return None
