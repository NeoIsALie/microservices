from fastapi import APIRouter

from privilege_service.routers import privilege, history

router = APIRouter()
router.include_router(privilege.router)
router.include_router(history.router)