import logging
import fastapi


class HTTPException(fastapi.HTTPException):
    """
    Custom HTTP exception class that logs its occurrence.
    """

    def __init__(
        self,
        status_code: int,
        detail: str = None,
        headers: dict = None,
        *,
        logger_name: str = __name__,
        logger_lvl: int = logging.WARNING,
        logger_msg: str = None,
    ) -> None:
        logging.getLogger(logger_name).log(
            level=logger_lvl,
            msg=f"HTTP {status_code} - {logger_msg or detail}",
            stacklevel=2,
        )
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )
