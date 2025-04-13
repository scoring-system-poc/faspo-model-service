import fastapi


router = fastapi.APIRouter(
    prefix="/probe",
    tags=["probe"],
)


@router.get("/alive")
async def alive() -> fastapi.responses.JSONResponse:
    """
    Health check endpoint to check if the service is alive.
    :return: fastapi.responses.JSONResponse
    """
    return fastapi.responses.JSONResponse(
        status_code=200,
        content={"detail": "Alive"},
    )


@router.get("/ready")
async def ready() -> fastapi.responses.JSONResponse:
    """
    Readiness check endpoint to check if the service is ready to process requests.
    :return: fastapi.responses.JSONResponse
    """
    return fastapi.responses.JSONResponse(
        status_code=200,
        content={"detail": "Ready"},
    )

