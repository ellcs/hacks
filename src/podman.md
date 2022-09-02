### run a podman container with binaries from host, without pulling an image 

This should work with docker too:

```bash
$ mkdir /tmp/empty
$ tar -C /tmp/empty -c . | podman import - emptybase
$ podman run -it -v /usr:/usr -v /bin:/bin -v /lib64:/lib64 emptybase /bin/bash
```

### pass nvidia gpu to container

```
# note that $container still needs the nvidia libs 
podman run --gpus all --device /dev/nvidia0 --device /dev/nvidia-uvm --device /dev/nvidia-uvm-tools --device /dev/nvidiactl -v $(pwd):/code -it $container  /bin/bash
```
