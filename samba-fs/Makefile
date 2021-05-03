.PHONY: run rm install

install:
	pip install -U pip setuptools wheel
	pip install -r requirements.txt


# SEE https://hub.docker.com/r/pwntr/samba-alpine/
run: DARGS?=
run:
	docker run $(DARGS) \
	-p 135:135/tcp -p 137:137/udp -p 138:138/udp -p 139:139/tcp -p 445:445/tcp \
	-v $(CURDIR)/configs/smb.conf:/config/smb.conf \
	-v $(CURDIR)/share/:/shared \
	--name samba pwntr/samba-alpine


rm:
	docker rm -f samba


tail:
	docker logs -f samba
