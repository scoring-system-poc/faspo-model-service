import pytest
import datetime as dt

from src.model.document import _DocumentType, _DocumentVersion, Document, FullDocument
from src.model.sheet import Sheet, _SheetInfo


@pytest.mark.asyncio
async def test_document_type():
    document_type = _DocumentType(
        key="123",
        name="Test Document Type",
        layer=1,
        order=2,
    )

    assert document_type.key == "123"
    assert document_type.name == "Test Document Type"
    assert document_type.layer == 1
    assert document_type.order == 2


@pytest.mark.asyncio
async def test_document_version():
    document_version = _DocumentVersion(
        version=1,
        author="Test Author",
        created="2023-10-01T12:00:00",
    )

    assert document_version.version == 1
    assert document_version.author == "Test Author"
    assert document_version.created == dt.datetime.fromisoformat("2023-10-01T12:00:00")


@pytest.mark.asyncio
async def test_document():
    document = Document(
        inner_type="doc",
        id="123",
        subject_id="456",
        type=_DocumentType(key="123", name="Test Document Type", layer=1, order=2),
        period="2023-10-01",
        version=_DocumentVersion(version=1, author="Test Author", created="2023-10-01T12:00:00"),
        sheets=[
            _SheetInfo(id="789", name="Test Sheet", number=1),
            _SheetInfo(id="101", name="Another Sheet", number=2),
        ],
    )

    assert document.inner_type == "doc"
    assert document.id == "123"
    assert document.subject_id == "456"
    assert document.type.key == "123"
    assert document.type.name == "Test Document Type"
    assert document.type.layer == 1
    assert document.type.order == 2
    assert document.period == dt.date.fromisoformat("2023-10-01")
    assert document.version.version == 1
    assert document.version.author == "Test Author"
    assert document.version.created == dt.datetime.fromisoformat("2023-10-01T12:00:00")
    assert len(document.sheets) == 2
    assert document.sheets[0].id == "789"
    assert document.sheets[0].name == "Test Sheet"
    assert document.sheets[0].number == 1
    assert document.sheets[1].id == "101"
    assert document.sheets[1].name == "Another Sheet"
    assert document.sheets[1].number == 2


@pytest.mark.asyncio
async def test_document_full():
    sheet = Sheet(
        id="123",
        subject_id="456",
        doc_id="789",
        name="Test Sheet",
        number=1,
        items=[
            [1, 2, 3],
            [4, 5, 6],
        ],
    )

    document = Document(
        inner_type="doc",
        id="123",
        subject_id="456",
        type=_DocumentType(key="123", name="Test Document Type", layer=1, order=2),
        period="2023-10-01",
        version=_DocumentVersion(version=1, author="Test Author", created="2023-10-01T12:00:00"),
        sheets=[sheet],
    )

    assert document.inner_type == "doc"
    assert document.id == "123"
    assert document.subject_id == "456"
    assert document.type.key == "123"
    assert document.type.name == "Test Document Type"
    assert document.type.layer == 1
    assert document.type.order == 2
    assert document.period == dt.date.fromisoformat("2023-10-01")
    assert document.version.version == 1
    assert document.version.author == "Test Author"
    assert document.version.created == dt.datetime.fromisoformat("2023-10-01T12:00:00")
    assert len(document.sheets) == 1
    assert len(document.sheets[0].items) == 2
    assert document.sheets[0].items[0] == [1, 2, 3]
    assert document.sheets[0].items[1] == [4, 5, 6]

