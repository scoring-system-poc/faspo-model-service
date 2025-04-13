import pytest
import datetime as dt

from src.core.exception import HTTPException
from src.service import score


@pytest.mark.asyncio
async def test_validate_input__success(mock_001_docs, mock_002_docs) -> None:
    assert score.validate_input([*mock_001_docs, *mock_002_docs])


@pytest.mark.asyncio
async def test_validate_input__missing_type(mock_001_docs) -> None:
    with pytest.raises(HTTPException) as excinfo:
        score.validate_input(mock_001_docs)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Missing required document type 002 for all periods"


@pytest.mark.asyncio
async def test_validate_input__missing_period(mock_001_docs, mock_002_docs) -> None:
    with pytest.raises(HTTPException) as excinfo:
        score.validate_input([*mock_001_docs[1:], *mock_002_docs])

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Missing required document type 001 for all periods"


@pytest.mark.asyncio
async def test_validate_input__not_consecutive_periods(mock_001_docs, mock_002_docs) -> None:
    with pytest.raises(HTTPException) as excinfo:
        mock_001_docs[0].period = dt.date(mock_001_docs[0].period.year - 1, 1, 1)
        score.validate_input([*mock_001_docs, *mock_002_docs])

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Missing required document type 001 for all periods"


@pytest.mark.asyncio
async def test_calculate_summary_document__success(mock_001_docs) -> None:
    summary = score.calculate_summary_document(mock_001_docs)

    assert summary.id is not None
    assert summary.subject_id == mock_001_docs[0].subject_id
    assert summary.type.key == "001S"
    assert summary.type.name == mock_001_docs[0].type.name + " - Summary"
    assert summary.type.layer == 2
    assert summary.type.order == mock_001_docs[0].type.order
    assert summary.period == mock_001_docs[-1].period
    assert summary.version.version == 1
    assert summary.version.author == "faspo-model-service"
    assert summary.version.created is not None

    assert len(summary.sheets) == len(mock_001_docs[0].sheets)

    assert summary.sheets[0].id is not None
    assert summary.sheets[0].subject_id == mock_001_docs[0].subject_id
    assert summary.sheets[0].doc_id == summary.id
    assert summary.sheets[0].name == mock_001_docs[0].sheets[0].name + " - Summary"
    assert summary.sheets[0].number == mock_001_docs[0].sheets[0].number
    assert summary.sheets[0].items == [["a", "b", 3.0, 6.0, 9.0, 12.0], ["c", "d", 15.0, 18.0, 21.0, 24.0]]

    assert summary.sheets[1].id is not None
    assert summary.sheets[1].subject_id == mock_001_docs[0].subject_id
    assert summary.sheets[1].doc_id == summary.id
    assert summary.sheets[1].name == mock_001_docs[0].sheets[1].name + " - Summary"
    assert summary.sheets[1].number == mock_001_docs[0].sheets[1].number
    assert summary.sheets[1].items == [["a", "b", 3.0, 6.0], ["c", "d", 9.0, 12.0]]


@pytest.mark.asyncio
async def test_calculate_summary_document__missing_period(mock_001_docs) -> None:
    with pytest.raises(HTTPException) as excinfo:
        score.calculate_summary_document(mock_001_docs[1:])

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Internal Server Error"


@pytest.mark.asyncio
async def test_calculate_summary_document__invalid_type(mock_003_docs) -> None:
    with pytest.raises(HTTPException) as excinfo:
        score.calculate_summary_document(mock_003_docs)

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Internal Server Error"


@pytest.mark.asyncio
async def test_calculate_scoring_documents__success(mock_001_docs, mock_002_docs) -> None:
    summary_001_doc = score.calculate_summary_document(mock_001_docs)
    summary_002_doc = score.calculate_summary_document(mock_002_docs)

    scoring_docs = score.calculate_scoring_documents([summary_001_doc, summary_002_doc])

    assert len(scoring_docs) == 4

    assert scoring_docs[0].id is not None
    assert scoring_docs[0].subject_id == summary_001_doc.subject_id
    assert scoring_docs[0].type.key == "SC1"
    assert scoring_docs[0].type.name == "Scoring document #1"
    assert scoring_docs[0].type.layer == 3
    assert scoring_docs[0].type.order == 1
    assert scoring_docs[0].period == summary_001_doc.period
    assert scoring_docs[0].version.version == 1
    assert scoring_docs[0].version.author == "faspo-model-service"
    assert scoring_docs[0].version.created is not None

    assert scoring_docs[1].type.key == "SC2"
    assert scoring_docs[1].type.name == "Scoring document #2"
    assert scoring_docs[1].type.order == 2

    for i in [0, 2, 3]:
        assert len(scoring_docs[i].sheets) == 1
        assert scoring_docs[i].sheets[0].items == [
            [11.25, 13.333333333333334, 15.0, 16.363636363636363],
            [14.625, 18.352941176470587, 21.666666666666668, 24.63157894736842],
        ]

    assert len(scoring_docs[1].sheets) == 1
    assert scoring_docs[1].sheets[0].items == [
        [5.142857142857143, 6.0],
        [7.636363636363637, 9.692307692307692],
    ]


@pytest.mark.asyncio
async def test_calculate_scoring_documents__missing_summary_doc(mock_001_docs) -> None:
    summary_001_doc = score.calculate_summary_document(mock_001_docs)

    with pytest.raises(HTTPException) as excinfo:
        score.calculate_scoring_documents([summary_001_doc])

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Internal Server Error"


@pytest.mark.asyncio
async def test_calculate_scoring_documents__invalid_type(mock_001_docs, mock_002_docs) -> None:
    summary_001_doc = score.calculate_summary_document(mock_001_docs)
    summary_002_doc = score.calculate_summary_document(mock_002_docs)
    summary_001_doc.type.key = "NOT_SUMMARY_DOC"

    with pytest.raises(HTTPException) as excinfo:
        score.calculate_scoring_documents([summary_001_doc, summary_002_doc])

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Internal Server Error"


@pytest.mark.asyncio
async def test_calculate_final_document__happy_path(mock_001_docs, mock_002_docs) -> None:
    summary_001_doc = score.calculate_summary_document(mock_001_docs)
    summary_002_doc = score.calculate_summary_document(mock_002_docs)

    scoring_docs = score.calculate_scoring_documents([summary_001_doc, summary_002_doc])
    final_scoring_doc = score.calculate_final_document(scoring_docs)

    assert final_scoring_doc.id is not None
    assert final_scoring_doc.subject_id == scoring_docs[0].subject_id
    assert final_scoring_doc.type.key == "FC"
    assert final_scoring_doc.type.name == "Final scoring"
    assert final_scoring_doc.type.layer == 4
    assert final_scoring_doc.type.order == 1
    assert final_scoring_doc.period == scoring_docs[0].period
    assert final_scoring_doc.version.version == 1
    assert final_scoring_doc.version.author == "faspo-model-service"
    assert final_scoring_doc.version.created is not None

    assert len(final_scoring_doc.sheets) == 1

    assert final_scoring_doc.sheets[0].id is not None
    assert final_scoring_doc.sheets[0].subject_id == scoring_docs[0].subject_id
    assert final_scoring_doc.sheets[0].doc_id == final_scoring_doc.id
    assert final_scoring_doc.sheets[0].name == "Final scoring"
    assert final_scoring_doc.sheets[0].number == 1

    assert final_scoring_doc.sheets[0].items == [
        [1, 'Subject has loans', False],
        [2, 'Loan amount', 0],
        [3, 'Subject has suspicious cashflow', False],
        [4, 'Cashflow', 0],
        [5, 'Capital', 0],
        [6, 'SC#1', 19.81904669762642],
        [7, 'SC#2', 8.664335664335663],
        [8, 'SC#3', 19.81904669762642],
        [9, 'SC#4', 19.81904669762642],
        [10, 'Final scoring', 42.605752587196086],
    ]


@pytest.mark.asyncio
async def test_calculate_final_document__happy_path_suspicious(mock_001_docs, mock_002_docs, mock_003_docs) -> None:
    summary_001_doc = score.calculate_summary_document(mock_001_docs)
    summary_002_doc = score.calculate_summary_document(mock_002_docs)

    scoring_docs = score.calculate_scoring_documents([summary_001_doc, summary_002_doc])
    final_scoring_doc = score.calculate_final_document(scoring_docs, cashflow_docs=mock_003_docs)

    assert final_scoring_doc.sheets[0].items == [
        [1, 'Subject has loans', False],
        [2, 'Loan amount', 0],
        [3, 'Subject has suspicious cashflow', True],
        [4, 'Cashflow', 201.0],
        [5, 'Capital', 12.0],
        [6, 'SC#1', 19.81904669762642],
        [7, 'SC#2', 8.664335664335663],
        [8, 'SC#3', 19.81904669762642],
        [9, 'SC#4', 19.81904669762642],
        [10, 'Final scoring', 25.515723170018838],
    ]


@pytest.mark.asyncio
async def test_calculate_final_document__happy_path_loans(mock_001_docs, mock_002_docs, mock_080_docs) -> None:
    summary_001_doc = score.calculate_summary_document(mock_001_docs)
    summary_002_doc = score.calculate_summary_document(mock_002_docs)

    scoring_docs = score.calculate_scoring_documents([summary_001_doc, summary_002_doc])
    final_scoring_doc = score.calculate_final_document(scoring_docs, loan_docs=mock_080_docs)

    assert final_scoring_doc.sheets[0].items == [
        [1, 'Subject has loans', True],
        [2, 'Loan amount', 1.0],
        [3, 'Subject has suspicious cashflow', False],
        [4, 'Cashflow', 0],
        [5, 'Capital', 0],
        [6, 'SC#1', 19.81904669762642],
        [7, 'SC#2', 8.664335664335663],
        [8, 'SC#3', 19.81904669762642],
        [9, 'SC#4', 19.81904669762642],
        [10, 'Final scoring', 34.06073787860746],
    ]


@pytest.mark.asyncio
async def test_calculate_final_document__happy_path_loans_suspicious(
    mock_001_docs,
    mock_002_docs,
    mock_003_docs,
    mock_080_docs,
) -> None:
    summary_001_doc = score.calculate_summary_document(mock_001_docs)
    summary_002_doc = score.calculate_summary_document(mock_002_docs)

    scoring_docs = score.calculate_scoring_documents([summary_001_doc, summary_002_doc])
    final_scoring_doc = score.calculate_final_document(
        scoring_docs,
        cashflow_docs=mock_003_docs,
        loan_docs=mock_080_docs,
    )

    assert final_scoring_doc.sheets[0].items == [
        [1, 'Subject has loans', True],
        [2, 'Loan amount', 1.0],
        [3, 'Subject has suspicious cashflow', True],
        [4, 'Cashflow', 201.0],
        [5, 'Capital', 12.0],
        [6, 'SC#1', 19.81904669762642],
        [7, 'SC#2', 8.664335664335663],
        [8, 'SC#3', 19.81904669762642],
        [9, 'SC#4', 19.81904669762642],
        [10, 'Final scoring', 22.66738493382263],
    ]


@pytest.mark.asyncio
async def test_calculate_final_document__missing_scoring_docs(mock_001_docs, mock_002_docs) -> None:
    summary_001_doc = score.calculate_summary_document(mock_001_docs)
    summary_002_doc = score.calculate_summary_document(mock_002_docs)

    scoring_docs = score.calculate_scoring_documents([summary_001_doc, summary_002_doc])

    with pytest.raises(HTTPException) as excinfo:
        score.calculate_final_document(scoring_docs[1:])

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Internal Server Error"


@pytest.mark.asyncio
async def test_calculate_final_document__incorrect_doc_type(mock_001_docs) -> None:
    with pytest.raises(HTTPException) as excinfo:
        score.calculate_final_document(mock_001_docs)

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Internal Server Error"


