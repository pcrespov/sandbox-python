FROM python-3.8 as base


RUN pip install --upgrade \
        pip \
        wheel\
        setuptool

WORKDIR /work
COPY scripts scripts
COPY src src
COPY requirements requirements

HEALTHCHECK \
    --interval=30s \
    --timeout=30s \
    --start-period=5s \
    --retries=3 \
    CMD [ "python", "scripts/health.py" ]


RUN pip install -r requirements/common.txt

WORKDIR /work/src

# ------------------------------
FROM base as aiohttp-app

RUN pip install -r requirements/aiohttp.txt

# ------------------------------
FROM base as fastapi-app

RUN pip install -r requirements/aiohttp.txt

ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0"]
