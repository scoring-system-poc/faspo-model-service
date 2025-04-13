import pytest

from src.model.sheet import _SheetInfo, Sheet


@pytest.mark.asyncio
async def test_sheet_info():
    sheet_info = _SheetInfo(
        id="123",
        name="Test name",
        number=1,
    )

    assert sheet_info.id == "123"
    assert sheet_info.name == "Test name"
    assert sheet_info.number == 1


@pytest.mark.asyncio
async def test_sheet():
    sheet = Sheet(
        id="123",
        name="Test name",
        number=1,
        subject_id="456",
        doc_id="789",
        items=[[1, 2, 3], ["a", "b", "c"], [None, None, None]],
    )

    assert sheet.inner_type == "sheet"
    assert sheet.id == "123"
    assert sheet.name == "Test name"
    assert sheet.number == 1
    assert sheet.subject_id == "456"
    assert sheet.doc_id == "789"
    assert sheet.items == [[1, 2, 3], ["a", "b", "c"], [None, None, None]]

