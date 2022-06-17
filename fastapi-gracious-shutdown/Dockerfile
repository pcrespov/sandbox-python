ARG PYTHON_VERSION="3.9.12"
FROM python:${PYTHON_VERSION}-slim-buster as base
#
#  USAGE:
#     cd sercices/dynamic-sidecar
#     docker build -f Dockerfile -t dynamic-sidecar:prod --target production ../../
#     docker run dynamic-sidecar:prod
#
#  REQUIRED: context expected at ``osparc-simcore/`` folder because we need access to osparc-simcore/packages


RUN set -eux && \
  apt-get update && \
  apt-get install -y \
  gosu \
  curl \
  && \
  rm -rf /var/lib/apt/lists/* && \
  # verify that the binary works
  gosu nobody true

# simcore-user uid=8004(scu) gid=8004(scu) groups=8004(scu)
ENV SC_USER_ID=8004 \
  SC_USER_NAME=scu \
  SC_BUILD_TARGET=base \
  SC_BOOT_MODE=default

RUN adduser \
  --uid ${SC_USER_ID} \
  --disabled-password \
  --gecos "" \
  --shell /bin/sh \
  --home /home/${SC_USER_NAME} \
  ${SC_USER_NAME}



# Sets utf-8 encoding for Python et al
ENV LANG=C.UTF-8

# Turns off writing .pyc files; superfluous on an ephemeral container.
ENV PYTHONDONTWRITEBYTECODE=1 \
  VIRTUAL_ENV=/home/scu/.venv

# Ensures that the python and pip executables used
# in the image will be those from our virtualenv.
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# directory where dynamic-sidecar stores creates and shares
# volumes between itself and the spawned containers
ENV DY_VOLUMES="/dy-volumes"


# -------------------------- Build stage -------------------
# Installs build/package management tools and third party dependencies
#
# + /build             WORKDIR
#
FROM base as build

ENV SC_BUILD_TARGET=build

RUN apt-get update &&\
  apt-get install -y --no-install-recommends \
  build-essential

# NOTE: python virtualenv is used here such that installed
# packages may be moved to production image easily by copying the venv
RUN python -m venv ${VIRTUAL_ENV}
RUN mkdir -p ${DY_VOLUMES}

RUN pip install --upgrade --no-cache-dir \
  pip~=22.0  \
  wheel \
  setuptools

WORKDIR /build

# NOTE: copies to /build to avoid overwriting later which would invalidate this layer
COPY --chown=scu:scu requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt


# --------------------------Production stage -------------------
# Final cleanup up to reduce image size and startup setup
# Runs as scu (non-root user)
#
#  + /home/scu     $HOME = WORKDIR
#    + services/dynamic-sidecar [scu:scu]
#
FROM base as production

ENV SC_BUILD_TARGET=production \
  SC_BOOT_MODE=production

ENV PYTHONOPTIMIZE=TRUE

WORKDIR /home/scu

# Starting from clean base image, copies pre-installed virtualenv
COPY --chown=scu:scu --from=build  ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --chown=scu:scu --from=build  ${DY_VOLUMES} ${DY_VOLUMES}
COPY --chown=scu:scu \
  "boot.sh" \
  "server.py" \
  "/home/scu/"


#uvicorn  --port INTEGER                  Bind socket to this port.  [default: 8000]
EXPOSE 8000
