import logging
import logging.config
import azure.monitor.opentelemetry
import azure.monitor.opentelemetry.exporter

from src.core.config import CONFIG


def setup_logging():
    """
    Set up logging configuration.
    """
    azure.monitor.opentelemetry.configure_azure_monitor(
        logger_name="src",
        instrumentation_options={
            "flask": {"enabled": False},
            "django": {"enabled": False},
            "psycopg2": {"enabled": False},
        }
    )

    logging.getLogger("uvicorn.access").addFilter(
        lambda record: record.getMessage().find("/probe/") == -1
    )

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation-id-filter": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 16,
                    "default_value": "0" * 16,
                },
            },
            "formatters": {
                "stdout-fmt": {
                    "class": "logging.Formatter",
                    "format": "%(asctime)s | %(levelname)-7s | %(name)-30s | %(funcName)-30s | %(correlation_id)-16s | %(message)s",
                },
            },
            "handlers": {
                "stdout-handler": {
                    "class": "logging.StreamHandler",
                    "filters": ["correlation-id-filter"],
                    "formatter": "stdout-fmt",
                },
            },
            "root": {"handlers": ["stdout-handler"], "level": CONFIG.LOG_LEVEL},
            "loggers": {
                "azure.monitor.opentelemetry": {"level": logging.WARNING},
                "azure.core.pipeline.policies.http_logging_policy": {"level": logging.WARNING},
            },
        }
    )

