
```cmd
docker \
Digest: sha256:05299e721cafd762e670dd9fdba3facb040a49ef5ec31fb2d1fd07b8524d8a9d
Status: Downloaded newer image for python:3
docker.io/library/python:3
DEBUG [job docker.cwl] initial work dir {}
INFO [job docker.cwl] /private/tmp/docker_tmpl_zoav6x$ docker \
    run \
    -i \
    # mounts HOME, TMPDIR
    
    --mount=type=bind,source=/private/tmp/docker_tmpl_zoav6x,target=/VmEnvV \
    --mount=type=bind,source=/private/tmp/docker_tmpw9lqooyb,target=/tmp \

    # mounts input file as READ ONLY!
    --mount=type=bind,source=/Users/pcrespov/devp/sandbox-python/cws/6/script.py,target=/var/lib/cwl/stg5842251d-d3d9-4e6e-b2ea-beedbf62de3c/script.py,readonly \
    
    --workdir=/VmEnvV \
    --read-only=true \
    --log-driver=none \
    --user=501:20 \
    --rm \
    --env=TMPDIR=/tmp \
    --env=HOME=/VmEnvV \
    --cidfile=/private/tmp/docker_tmp6nhhgkl5/20201008163948-497154.cid \
    python:3 \
    python \
    /var/lib/cwl/stg5842251d-d3d9-4e6e-b2ea-beedbf62de3c/script.py > /private/tmp/docker_tmpl_zoav6x/output.txt
INFO [job docker.cwl] Max memory used: 0MiB
INFO [job docker.cwl] completed success
DEBUG [job docker.cwl] outputs {
    "example_out": {
        "location": "file:///private/tmp/docker_tmpl_zoav6x/output.txt",
        "basename": "output.txt",
        "nameroot": "output",
        "nameext": ".txt",
        "class": "File",
        "checksum": "sha1$cf8db7e6374c15ada0989e8d347ff37d3620cd74",
        "size": 29,
        "http://commonwl.org/cwltool#generation": 0
    }
}
DEBUG [job docker.cwl] Removing input staging directory /private/tmp/docker_tmpgk22yxgv
DEBUG [job docker.cwl] Removing temporary directory /private/tmp/docker_tmpw9lqooyb
DEBUG Moving /private/tmp/docker_tmpl_zoav6x/output.txt to /Users/pcrespov/devp/sandbox-python/cws/6/output.txt
{
    "example_out": {
        "location": "file:///Users/pcrespov/devp/sandbox-python/cws/6/output.txt",
        "basename": "output.txt",
        "class": "File",
        "checksum": "sha1$cf8db7e6374c15ada0989e8d347ff37d3620cd74",
        "size": 29,
        "path": "/Users/pcrespov/devp/sandbox-python/cws/6/output.txt"
    }
}
INFO Final process status is success
```