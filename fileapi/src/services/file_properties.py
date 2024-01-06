from abc import ABC, abstractmethod

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.file_properties import FileProperties, FilePropertiesCreate


class FilePropertiesServiceABC(ABC):
    """Abstract base class for file properties storage."""

    @abstractmethod
    async def save(self, *args, **kwargs) -> FileProperties:
        ...

    @abstractmethod
    async def get(self, *args, **kwargs) -> FileProperties:
        ...


class FilePropertiesService(FilePropertiesServiceABC):
    """Class implementing postgres based file properties storage."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def save(
        self, file_properties: FilePropertiesCreate
    ) -> FileProperties:
        """
        Save file properties to the database.
        """
        db_file_properties = FileProperties.model_validate(file_properties)
        self.db_session.add(db_file_properties)
        await self.db_session.commit()
        await self.db_session.refresh(db_file_properties)
        return db_file_properties

    async def get(self, short_name: str) -> FileProperties:
        """
        Get file properties by short name from the database.
        """
        query = select(FileProperties).where(
            FileProperties.short_name == short_name
        )
        result = await self.db_session.exec(query)
        file_properties = result.one_or_none()
        return file_properties
