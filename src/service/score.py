import logging
import secrets
import datetime as dt

from src.core.config import CONFIG
from src.core.exception import HTTPException
from src.model.document import FullDocument
from src.model.sheet import Sheet


def validate_input(docs: list[FullDocument]) -> bool:
    """
    Simulate validation of input payload - i.e. if it all contains mandatory document
    :param docs: List of Document objects
    :return: True if validation is successful, raises HTTPException otherwise
    """
    periods = dict()

    for doc in docs:
        periods[doc.type.key] = periods.get(doc.type.key, set()).union({doc.period.year})

    for required_doc in CONFIG.REQUIRED_DOCUMENT_TYPES:
        if (
            len(periods.get(required_doc, set())) != CONFIG.REQUIRED_DOCUMENT_PERIODS
            or
            max(periods[required_doc]) != min(periods[required_doc]) + CONFIG.REQUIRED_DOCUMENT_PERIODS - 1
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Missing required document type {required_doc} for all periods",
                logger_name=__name__,
            )

    return True


def calculate_summary_document(docs: list[FullDocument]) -> FullDocument:
    """
    WARNING: all calculations are completely made up and from bussiness point of view nonsensical

    Simulate calculation of summary document - i.e. sum of mandatory periods for each document type
    :param docs: List of Document objects (all of the same bussiness type)
    :return: Document object with summary data
    """
    if len(docs) != CONFIG.REQUIRED_DOCUMENT_PERIODS or docs[0].type.key not in CONFIG.REQUIRED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=500,
            logger_name=__name__,
            logger_lvl=logging.ERROR,
            logger_msg="Invalid input data - not all required documents are present",
        )

    doc_id = secrets.token_hex(16)
    sheets = []

    for sheet_num in range(len(docs[0].sheets)):
        sheet_data = []

        cols = len(docs[0].sheets[sheet_num].items[0])
        rows = len(docs[0].sheets[sheet_num].items)

        for i in range(rows):
            row_data = []

            for j in range(2):
                row_data.append(docs[0].sheets[sheet_num].items[i][j])

            for j in range(2, cols):
                row_data.append(sum(doc.sheets[sheet_num].items[i][j] for doc in docs))

            sheet_data.append(row_data)

        sheets.append(
            Sheet(
                id=secrets.token_hex(16),
                subject_id=docs[0].subject_id,
                doc_id=doc_id,
                name=f"{docs[0].sheets[sheet_num].name} - Summary",
                number=docs[0].sheets[sheet_num].number,
                items=sheet_data,
            )
        )

    return FullDocument(
        id=doc_id,
        subject_id=docs[0].subject_id,
        type={
            "key": f"{docs[0].type.key}S",
            "name": f"{docs[0].type.name} - Summary",
            "layer": 2,
            "order": docs[0].type.order,
        },
        period=max(doc.period for doc in docs),
        version={
            "version": 1,
            "author": "faspo-model-service",
            "created": dt.datetime.now(),
        },
        sheets=sheets,
    )


def calculate_scoring_documents(summary_docs: list[FullDocument]) -> list[FullDocument]:
    """
    WARNING: all calculations are completely made up and from bussiness point of view nonsensical

    Simulate calculation of scoring document
    :param summary_docs: List of Document objects (of summary type)
    :return: List of Document objects with scoring data
    """
    if (
        len(summary_docs) != len(CONFIG.REQUIRED_DOCUMENT_TYPES)
        or
        not all(doc.type.key[-1] == "S" for doc in summary_docs)
    ):
        raise HTTPException(
            status_code=500,
            logger_name=__name__,
            logger_lvl=logging.ERROR,
            logger_msg="Invalid input data - not all required documents are present",
        )

    docs = []

    for doc in summary_docs:
        for sheet in doc.sheets:
            doc_id = secrets.token_hex(16)

            col_sums = [sum(col) for col in list(zip(*sheet.items))[2:]]
            row_sums = [sum(row[2:]) for row in sheet.items]
            cross_product = [[(r * c / (r + c)) if (r + c) else float("nan") for c in col_sums] for r in row_sums]

            docs.append(
                FullDocument(
                    id=doc_id,
                    subject_id=doc.subject_id,
                    type={
                        "key": f"SC{len(docs) + 1}",
                        "name": f"Scoring document #{len(docs) + 1}",
                        "layer": 3,
                        "order": len(docs) + 1,
                    },
                    period=doc.period,
                    version={
                        "version": 1,
                        "author": "faspo-model-service",
                        "created": dt.datetime.now(),
                    },
                    sheets=[
                        Sheet(
                            id=secrets.token_hex(16),
                            subject_id=doc.subject_id,
                            doc_id=doc_id,
                            name="Scoring",
                            number=1,
                            items=cross_product,
                        )
                    ],
                )
            )

    return docs


def calculate_final_document(
    scoring_docs: list[FullDocument],
    *,
    cashflow_docs: list[FullDocument] = None,
    loan_docs: list[FullDocument] = None,
) -> FullDocument:
    """
    WARNING: all calculations are completely made up and from bussiness point of view nonsensical

    Simulate calculation of final document
    :param scoring_docs: List of Document objects (of scoring type)
    :param cashflow: List of Document objects (additional data from input)
    :param loans: List of Document objects (additional data from input)
    :return: Document object with final data
    """
    if (
        len(scoring_docs) != 4
        or
        not all(doc.type.key.startswith("SC") for doc in scoring_docs)
    ):
        raise HTTPException(
            status_code=500,
            logger_name=__name__,
            logger_lvl=logging.ERROR,
            logger_msg="Invalid input data - not all required documents are present",
    )

    subject_has_loans = bool(loan_docs)
    loans_sum = sum(row[5] for doc in loan_docs for row in doc.sheets[0].items) if subject_has_loans else 0

    cashflow_sum = sum(row[1] for doc in cashflow_docs for row in doc.sheets[0].items) if cashflow_docs else 0
    capital_sum = sum(row[4] for doc in cashflow_docs for row in doc.sheets[1].items) if cashflow_docs else 0
    subject_is_suspicious = cashflow_sum > capital_sum * 10

    scoring_1_avg = sum(scoring_docs[0].sheets[0].items[-1]) / len(scoring_docs[0].sheets[0].items[-1])
    scoring_2_avg = sum(scoring_docs[1].sheets[0].items[-1]) / len(scoring_docs[1].sheets[0].items[-1])
    scoring_3_avg = sum(scoring_docs[2].sheets[0].items[-1]) / len(scoring_docs[2].sheets[0].items[-1])
    scoring_4_avg = sum(scoring_docs[3].sheets[0].items[-1]) / len(scoring_docs[3].sheets[0].items[-1])

    coefficient = 0
    final_scoring = 0

    if subject_has_loans and subject_is_suspicious:
        coefficient = .1
    elif not subject_has_loans and subject_is_suspicious:
        coefficient = .2
    elif subject_has_loans and not subject_is_suspicious:
        coefficient = .5
    else:
        coefficient = .8

    final_scoring += scoring_1_avg * coefficient
    final_scoring += scoring_2_avg * coefficient
    final_scoring += scoring_3_avg * (1 - coefficient)
    final_scoring += scoring_4_avg * coefficient

    doc_id = secrets.token_hex(16)
    return FullDocument(
        id=doc_id,
        subject_id=scoring_docs[0].subject_id,
        type={
            "key": "FC",
            "name": "Final scoring",
            "layer": 4,
            "order": 1,
        },
        period=scoring_docs[0].period,
        version={
            "version": 1,
            "author": "faspo-model-service",
            "created": dt.datetime.now(),
        },
        sheets=[
            Sheet(
                id=secrets.token_hex(16),
                subject_id=scoring_docs[0].subject_id,
                doc_id=doc_id,
                name="Final scoring",
                number=1,
                items=[
                    [1, "Subject has loans", subject_has_loans],
                    [2, "Loan amount", loans_sum],
                    [3, "Subject has suspicious cashflow", subject_is_suspicious],
                    [4, "Cashflow", cashflow_sum],
                    [5, "Capital", capital_sum],
                    [6, "SC#1", scoring_1_avg],
                    [7, "SC#2", scoring_2_avg],
                    [8, "SC#3", scoring_3_avg],
                    [9, "SC#4", scoring_4_avg],
                    [10, "Final scoring", final_scoring],
                ],
            )
        ],
    )

