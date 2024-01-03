FROM python:3

ENV DJANGO_SETTINGS_MODULE 'config.settings.dev'

WORKDIR /code/

RUN apt-get update && apt-get install -y gettext

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
