import pydantic
import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    """
    Environment configuration for the application.
    """
    # Data Target
    DATA_TARGET_URL: str = "http://faspo-store-service/api/v1/document"

    # Constants
    REQUIRED_DOCUMENT_TYPES: list[str] = ["001", "002"]
    REQUIRED_DOCUMENT_PERIODS: int = 3
    OPTIONAL_CASHFLOW_DOCUMENT_TYPE: str = "003"
    OPTIONAL_LOAN_DOCUMENT_TYPE: str = "080"

    # General
    LOG_LEVEL: pydantic.constr(to_upper=True) = "INFO"


CONFIG = Config()
