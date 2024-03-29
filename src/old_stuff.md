#  Old stuff

### mount image file via loop device

https://web.archive.org/web/20210630122026/https://superuser.com/questions/344899/how-can-i-mount-a-disk-image


### mount image file without root permissions

https://web.archive.org/web/20210428082118/https://unix.stackexchange.com/questions/32008/how-to-mount-an-image-file-without-root-permission
```shell
# create mount target
mkdir mnt   

# try automount, fails if multiple partitions
guestmount -a image.iso -r -i mnt

# mount partition explicit (sda1 is not a real device)
guestmount -a image.iso -r -m /dev/sda1 --ro mnt

# unmount the guestmount (Not shown in lsblk!)
guestunmount mnt
```


### ssh with old algos

```
ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 123.123.123.123
```



### download subtitles with youtube-dl

```bash
youtube-dl --list-subs https://www.youtube.com/watch?v=dl78PQGJpiI

youtube-dl --all-subs --skip-download https://www.youtube.com/watch?v=dl78PQGJpiI
```

### grep for base64 like strings

https://unix.stackexchange.com/questions/542428/can-you-search-for-base64-with-grep#542433

```bash
grep -En '[[:alnum:]/+]{20,}' file
grep -E '[A-Za-z0-9+/]{4}*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)'
```

### procfs && working with file descriptors

```bash
bash -c 'grep heap /proc/$$/maps'
diff /proc/self/fd/3 /proc/self/fd/4 4<<<"$(xxd a)" 3<<<"$(xxd b)"
cat /proc/self/fd/4 4<<<"asdfasdf"
```

### laggy tigervnc session

```bash
vncviewer -Shared -CompressLevel 9 -via ellcs@hostname :1
```

### git push local branch to remote with same name

```bash
git push -u origin $(git branch | grep '*' | sed 's/* //')
```
