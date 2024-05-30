FROM python:3.12

WORKDIR  /fastapi

COPY /pyproject.toml /fastapi

RUN pip3 install poetry==1.7.1
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /fastapi

WORKDIR  /fastapi