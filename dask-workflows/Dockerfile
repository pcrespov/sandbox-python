ARG PYTHON_VERSION="3.6.10"
FROM python:${PYTHON_VERSION}-slim-buster as base


RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    curl \
    graphviz \
    git \
    iputils-ping \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN pip --no-cache-dir install --upgrade \
    pip\
    setuptools\
    wheel \
    && pip --no-cache-dir install \
    "fastapi[all]" \
    "uvicorn[standard]" \
    # TODO: Careful. this is more optimized and different naming with conda!
    "dask[complete]" \
    graphviz \
    && pip --no-cache-dir list -vv

WORKDIR /app

