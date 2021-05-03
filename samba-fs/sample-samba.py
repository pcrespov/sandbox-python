from datetime import datetime
from pprint import pprint

import fs
import fs.smbfs

# SEE https://hub.docker.com/r/pwntr/samba-alpine/
user = "rio"
password = "letsdance"
host = "127.0.0.1"

# docker run -d --network host -v $(PWD)/share/:/shared --name samba pwntr/samba-alpine

assert user
assert password

with fs.open_fs(f"smb://{user}:{password}@{host}/") as smb_fs:

    smb_fs.makedirs("/data/foo", recreate=True)
    with smb_fs.open("/data/foo/test.txt", "at") as f:
        f.write(datetime.now().isoformat())

    smb_fs.tree(path="/")

    info = smb_fs.getinfo(path="/data/foo", namespaces=["details", "access"])
    print(info)
    print(info.name, info.type, info.uid, info.gid, info.accessed)
    print(info.namespaces)
    print(info.permissions)
