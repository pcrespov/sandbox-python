#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/

set -o errexit
set -o nounset
set -o pipefail
IFS=$'\n\t'

IMAGE_NAME="local/pytest-cli:latest"
WORKDIR="$(pwd)"

run() {
  docker run \
    -it \
    --rm \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --user="$(id --user "$USER")":"$(id --group "$USER")" \
    --volume "$WORKDIR":/work \
    --workdir=/work \
    "$IMAGE_NAME" \
    "$@"
}

shell() {
  docker run \
    -it \
    --rm \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --user="$(id --user "$USER")":"$(id --group "$USER")" \
    --volume "$WORKDIR":/work \
    --workdir=/work \
    --entrypoint=bash \
    "$IMAGE_NAME"
}

# ----------------------------------------------------------------------
# =========================================================================== warnings summary ============================================================================
#
# Permissions!!! issue! with caches and all that!
#
# ../home/scu/.venv/lib/python3.9/site-packages/_pytest/cacheprovider.py:433
#   /home/scu/.venv/lib/python3.9/site-packages/_pytest/cacheprovider.py:433: PytestCacheWarning: could not create cache path /.pytest_cache/v/cache/nodeids
#     config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

# ../home/scu/.venv/lib/python3.9/site-packages/_pytest/stepwise.py:52
#   /home/scu/.venv/lib/python3.9/site-packages/_pytest/stepwise.py:52: PytestCacheWarning: could not create cache path /.pytest_cache/v/cache/stepwise
#     session.config.cache.set(STEPWISE_CACHE_DIR, [])

# -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

run "$@"
## shell
# ----------------------------------------------------------------------
