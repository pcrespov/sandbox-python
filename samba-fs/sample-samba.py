from pprint import pprint
from datetime import datetime
import fs
import fs.smbfs


# SEE https://hub.docker.com/r/pwntr/samba-alpine/
user = "rio"
password = "letsdance"
host = "127.0.0.1"

# docker run -d --network host -v $(PWD)/share/:/shared --name samba pwntr/samba-alpine

assert user
assert password

with fs.open_fs(f'smb://{user}:{password}@{host}/') as smb_fs:
    smb_fs.tree(path="/")

    smb_fs.makedir("foo")

    info = smb_fs.getinfo(path="/", namespaces=['details', 'access'])
    pprint(info)
