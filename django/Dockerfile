FROM python:3

ENV DJANGO_SETTINGS_MODULE 'config.settings.dev'

WORKDIR /code/

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
