import aiohttp
import pydantic

from src.core.config import CONFIG
from src.core.exception import HTTPException


async def post_data(data: pydantic.BaseModel, correlation_id: str | None = None) -> str:
    """
    Post data to the data target API (store-service most likely).
    :param data: Data to be posted, should be a Pydantic model.
    :param correlation_id: Correlation ID for tracing the request.
    :return: Response text from the API (ID of created item).
    """
    async with (
        aiohttp.ClientSession() as async_session,
        async_session.post(
            url=f"{CONFIG.DATA_TARGET_URL}",
            headers={"Correlation-Id": correlation_id},
            json=data.model_dump(mode="json", by_alias=True),
        ) as response,
    ):
        if response.status != 201:
            raise HTTPException(
                status_code=response.status,
                detail=f"Data target API request failed: {response.reason}",
                logger_name=__name__,
            )

        return await response.text()
