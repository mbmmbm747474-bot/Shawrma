from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    roles,
    permissions,
    companies,
    branches,
    dashboard,
)

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

api_router.include_router(
    roles.router,
    prefix="/roles",
    tags=["Roles"],
)

api_router.include_router(
    permissions.router,
    prefix="/permissions",
    tags=["Permissions"],
)

api_router.include_router(
    companies.router,
    prefix="/companies",
    tags=["Companies"],
)

api_router.include_router(
    branches.router,
    prefix="/branches",
    tags=["Branches"],
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
)
