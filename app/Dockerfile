FROM python:3.8.0-alpine

ENV APP_PATH /usr/src/app
WORKDIR $APP_PATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev
RUN pip install --upgrade pip
RUN pip install django-cors-headers
RUN pip install django-adminlte3

COPY ./requirements.txt $APP_PATH/
RUN pip install --no-cache-dir -r $APP_PATH/requirements.txt

COPY ./ ./