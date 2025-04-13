import fastapi
import contextlib
import asgi_correlation_id

from src.core.logging import setup_logging
from src.api.v1 import router as v1_api_router


@contextlib.asynccontextmanager
async def _lifespan(*args, **kwargs):
    setup_logging()
    yield


app = fastapi.FastAPI(lifespan=_lifespan)
app.add_middleware(asgi_correlation_id.CorrelationIdMiddleware, header_name="correlation-id", validator=None)

app.include_router(v1_api_router)


@app.get("/", include_in_schema=False, response_class=fastapi.responses.RedirectResponse)
async def api_spec():
    return "/docs"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=None)

