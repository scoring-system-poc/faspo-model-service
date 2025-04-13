import fastapi

from .probe import router as probe_router
from .score import router as score_router


router = fastapi.APIRouter(
    prefix="/api/v1",
)

router.include_router(probe_router)
router.include_router(score_router)
