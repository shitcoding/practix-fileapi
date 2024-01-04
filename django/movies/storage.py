import requests

from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.uploadedfile import InMemoryUploadedFile


class CustomStorage(Storage):
    def _save(self, name, content: InMemoryUploadedFile):
        url = f'{settings.FILEAPI_HOST}{settings.FILEAPI_UPLOAD_URL}'
        r = requests.post(
            url=url,
            files={'file': (content.name, content, content.content_type)},
        )
        return r.json().get('file_properties').get('short_name')

    def url(self, short_name):
        return f'{settings.FILEAPI_DOWNLOAD_URL}{short_name}'

    def exists(self, short_name):
        return False
