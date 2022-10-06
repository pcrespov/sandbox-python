# FROM registry.osparc-master.speag.com/simcore/services/dynamic/jupyter-octave-python-math:1.6.9
FROM python:3.9.12-slim-buster


WORKDIR /work
COPY . /work
RUN pip install -U pip \
    && pip install -r requirements.txt


# install osparc-binder-program
# install user scripts
