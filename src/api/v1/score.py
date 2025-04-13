import typing
import logging
import fastapi

from src.core.config import CONFIG
from src.core.exception import HTTPException
from src.model.document import FullDocument, Document
from src.service import score, data_target


logger = logging.getLogger(__name__)
router = fastapi.APIRouter(
    tags=["score"],
)


@router.post("/score")
def score_(
    docs: typing.Annotated[list[FullDocument], fastapi.Body()],
    background_tasks: fastapi.BackgroundTasks,
    correlation_id: typing.Annotated[str | None, fastapi.Header()] = None,
) -> fastapi.responses.JSONResponse:
    """
    Score.
    :param docs: List of documents input documents used for scoring.
    :param correlation_id: Correlation ID for tracing.
    :return: ID of created final scoring document.
    """
    logger.info(f"acquired request {correlation_id}")
    try:
        score.validate_input(docs)
        logger.info("input validation successful")

        mandatory_docs = [
            list(
                filter(lambda x: x.type.key == doc_type, docs)
            )
            for doc_type in CONFIG.REQUIRED_DOCUMENT_TYPES
        ]
        cashflow_docs = list(
            filter(lambda x: x.type.key == CONFIG.OPTIONAL_CASHFLOW_DOCUMENT_TYPE, docs)
        )
        loan_docs = list(
            filter(lambda x: x.type.key == CONFIG.OPTIONAL_LOAN_DOCUMENT_TYPE, docs)
        )

        summary_docs = [score.calculate_summary_document(docs) for docs in mandatory_docs]
        logger.info("summary document calculation successful")

        scoring_docs = score.calculate_scoring_documents(summary_docs)
        logger.info("scoring document calculation successful")

        final_doc = score.calculate_final_document(scoring_docs, cashflow_docs=cashflow_docs, loan_docs=loan_docs)
        logger.info("final document calculation successful")

        for doc in [*summary_docs, *scoring_docs, final_doc]:
            background_tasks.add_task(data_target.post_data, Document(**doc.model_dump()), correlation_id)
            for sheet in doc.sheets:
                background_tasks.add_task(data_target.post_data, sheet, correlation_id)

        return fastapi.responses.JSONResponse(
            content={"id": final_doc.id},
            status_code=201,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            logger_name=__name__,
            logger_lvl=logging.ERROR,
            logger_msg=f"scoring failed due to unexpected error: {str(e)}",
        )

