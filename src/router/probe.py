import logging
import fastapi


logger = logging.getLogger(__name__)
router = fastapi.APIRouter(
    tags=["probe"]
)


@router.get("/alive")
async def alive():
    return "alive"


@router.get("/ready")
async def ready():
    return "ready"
