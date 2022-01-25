ARG PYTHON_VERSION="3.8.10"
FROM python:${PYTHON_VERSION}-slim-buster as base


RUN pip install --upgrade pip setuptools wheel && \
    pip install \
        fastapi \
        uvicorn

