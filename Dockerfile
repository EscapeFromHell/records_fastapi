FROM python:3.11

RUN mkdir /src

COPY ./ /src

WORKDIR /src

ENV PYTHONPATH=/src

RUN apt-get update && apt-get install -y ffmpeg

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install
