from functools import cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_db_session
from dependencies.registrator import add_factory_to_mapper
from services.file_properties import (FilePropertiesService,
                                      FilePropertiesServiceABC)


@add_factory_to_mapper(FilePropertiesServiceABC)
@cache
def create_file_properties_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> FilePropertiesService:
    return FilePropertiesService(db_session)
