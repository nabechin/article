FROM python:3.8.0-alpine

ENV APP_PATH /usr/src/app
WORKDIR $APP_PATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libffi-dev libressl-dev
RUN pip install --upgrade pip

COPY ./requirements.txt $APP_PATH/
RUN pip install -r $APP_PATH/requirements.txt

COPY ./ ./