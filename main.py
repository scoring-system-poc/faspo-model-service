import logging
import fastapi
import azure.monitor.opentelemetry

from src.router import probe


logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
azure.monitor.opentelemetry.configure_azure_monitor(logger_name="src")


app = fastapi.FastAPI()
app.include_router(probe.router)


@app.get("/", include_in_schema=False, response_class=fastapi.responses.RedirectResponse)
async def api_spec():
    return "/docs"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
