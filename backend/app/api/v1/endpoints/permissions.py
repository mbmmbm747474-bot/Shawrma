from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.role import Permission
from app.models.user import User
from app.schemas.role import PermissionResponse

router = APIRouter()


@router.get("/", response_model=list[PermissionResponse])
def list_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    module: str | None = None,
) -> Any:
    query = db.query(Permission)
    if module:
        query = query.filter(Permission.module == module)
    return query.order_by(Permission.module, Permission.action).all()
