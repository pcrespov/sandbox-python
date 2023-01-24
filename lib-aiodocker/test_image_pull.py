# pylint:disable=unused-variable
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name
# pylint:disable=too-many-arguments
# pylint: disable=not-async-context-manager

# https://aiodocker.readthedocs.io/en/latest/index.html

from enum import Enum
from typing import TypedDict

import aiodocker
import pytest


class _PULL_PROGRESS_STATES(str, Enum):
    DOWNLOADING = "Downloading"
    DOWNLOAD_COMPLETE = "Download complete"
    EXTRACTING = "Extracting"
    PULL_COMPLETE = "Pull complete"


@pytest.mark.skip()
def test_it():

    assert "Downloading" in list(_PULL_PROGRESS_STATES)

    assert "Download complete" == _PULL_PROGRESS_STATES.DOWNLOAD_COMPLETE


async def test_docker_client(event_loop):
    async with aiodocker.Docker() as client:
        async for pull_progress in client.images.pull(
            "ubuntu:latest",
            stream=True,
            # auth={"username": "admin", "password": "adminadmin"},
        ):
            print(pull_progress)


#
# EXAMPLES:
#
# {'status': 'Pulling fs layer', 'progressDetail': {}, 'id': '6e3729cf69e0'}
# {'status': 'Downloading', 'progressDetail': {'current': 309633, 'total': 30428708}, 'progress': '[>                                                  ]  309.6kB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Status: Downloaded newer image for ubuntu:latest'}
# {'status': 'Verifying Checksum', 'progressDetail': {}, 'id': '6e3729cf69e0'}
# {'status': 'Pull complete', 'progressDetail': {}, 'id': '6e3729cf69e0'}
# {'status': 'Downloading', 'progressDetail': {'current': 4663681, 'total': 30428708}, 'progress': '[=======>                                           ]  4.664MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Downloading', 'progressDetail': {'current': 5912961, 'total': 30428708}, 'progress': '[=========>                                         ]  5.913MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Downloading', 'progressDetail': {'current': 8718721, 'total': 30428708}, 'progress': '[==============>                                    ]  8.719MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Downloading', 'progressDetail': {'current': 11204993, 'total': 30428708}, 'progress': '[==================>                                ]   11.2MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Downloading', 'progressDetail': {'current': 15563137, 'total': 30428708}, 'progress': '[=========================>                         ]  15.56MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Downloading', 'progressDetail': {'current': 23361921, 'total': 30428708}, 'progress': '[======================================>            ]  23.36MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Download complete', 'progressDetail': {}, 'id': '6e3729cf69e0'}
# {'status': 'Extracting', 'progressDetail': {'current': 327680, 'total': 30428708}, 'progress': '[>                                                  ]  327.7kB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Extracting', 'progressDetail': {'current': 7864320, 'total': 30428708}, 'progress': '[============>                                      ]  7.864MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Extracting', 'progressDetail': {'current': 13434880, 'total': 30428708}, 'progress': '[======================>                            ]  13.43MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Extracting', 'progressDetail': {'current': 21626880, 'total': 30428708}, 'progress': '[===================================>               ]  21.63MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Extracting', 'progressDetail': {'current': 26542080, 'total': 30428708}, 'progress': '[===========================================>       ]  26.54MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Extracting', 'progressDetail': {'current': 30146560, 'total': 30428708}, 'progress': '[=================================================> ]  30.15MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Extracting', 'progressDetail': {'current': 30428708, 'total': 30428708}, 'progress': '[==================================================>]  30.43MB/30.43MB', 'id': '6e3729cf69e0'}
# {'status': 'Digest: sha256:27cb6e6ccef575a4698b66f5de06c7ecd61589132d5a91d098f7f3f9285415a9'}


class ProgressDetailDict(TypedDict, total=False):
    current: int
    total: int


class PullProgressInfoDictq(TypedDict, total=True):
    id: str
    status: str
    progressDetail: ProgressDetailDict
    progress: str
