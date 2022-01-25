#!/bin/sh
set -o errexit
set -o nounset

IFS=$(printf '\n\t')

pip --no-cache-dir install -e .


exec uvicorn simcore_service_director_v2.main:the_app \
    --host 0.0.0.0 \
    --reload \
    --reload-dir simple-app/src/simple_app