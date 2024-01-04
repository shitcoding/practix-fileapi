import uuid
from datetime import datetime
from typing import Optional

from pydantic.types import PositiveInt
from sqlmodel import Column, DateTime, Field, SQLModel


class FilePropertiesBase(SQLModel):
    """
    Base data model of file properties entry.
    Serves as pydantic model for data validation.
    """

    path_in_storage: str = Field(unique=True, max_length=255, index=True)
    filename: str = Field(max_length=255)
    size: PositiveInt
    file_type: Optional[str] = Field(default=None, max_length=100)
    short_name: str = Field(unique=True, max_length=24, index=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=datetime.utcnow,
    )


class FileProperties(FilePropertiesBase, table=True):
    """
    Model of the `file_properties` db table.
    `id` is optional because it's autocreated by database.
    """

    __tablename__ = 'file_properties'
    __table_args__ = {'schema': 'file_api'}

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True
    )

    def __repr__(self) -> str:
        return f'<FileProperties id={self.id}>'


class FilePropertiesCreate(FilePropertiesBase):
    """Data model for creating a file properties db entry."""

    pass


class FilePropertiesRead(FilePropertiesBase):
    """Data model for file properties entry api response."""

    id: uuid.UUID


class FilePropertiesUpdate(SQLModel):
    """
    Data model for updating a file properties db entry.
    All fields are optional to be able to update any of them.
    """

    path_in_storage: Optional[str] = None
    filename: Optional[str] = None
    size: Optional[PositiveInt] = None
    file_type: Optional[str] = None
    short_name: Optional[str] = None
    created_at: Optional[datetime] = None
