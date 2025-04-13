import pydantic
import datetime as dt

from src.model.sheet import Sheet, _SheetInfo


class _DocumentType(pydantic.BaseModel):
    """
    Generic document type information
    """
    key: str
    name: str
    layer: int
    order: int


class _DocumentVersion(pydantic.BaseModel):
    """
    Specific document version information
    """
    version: int
    author: str
    created: dt.datetime


class Document(pydantic.BaseModel):
    """
    Document data
    """
    inner_type: str = pydantic.Field(default="doc", alias="_type", serialization_alias="_type")
    id: str
    subject_id: str
    type: _DocumentType
    period: dt.date
    version: _DocumentVersion
    sheets: list[_SheetInfo]     # actual sheet data are stored separately (because of size)


class FullDocument(Document):
    """
    Full document with all its data (including sheets)
    """
    sheets: list[Sheet]

