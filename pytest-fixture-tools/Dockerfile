FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends graphviz \
    && rm -rf /var/lib/apt/lists/*

RUN  pip --no-cache-dir install --upgrade pip setuptools wheel \
    && pip --no-cache-dir install \
    pyparsing \
    pydot \
    pytest-fixture-tools
