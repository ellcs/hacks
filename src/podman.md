### run a podman container with binaries from host, without pulling an image 

This should work with docker too:

```bash
$ mkdir /tmp/empty
$ tar -C /tmp/empty -c . | podman import - emptybase
$ podman run -it -v /usr:/usr -v /bin:/bin -v /lib64:/lib64 emptybase /bin/bash
```
