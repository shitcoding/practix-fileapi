from db.postgres import get_session
from fastapi import Depends
from models.file_properties import FileProperties, FilePropertiesCreate
from services.base import BaseService
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class FilePropertiesService(BaseService):
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


def get_file_properties_service(
    db_session: AsyncSession = Depends(get_session),
) -> FilePropertiesService:
    return FilePropertiesService(db_session)
