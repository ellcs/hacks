### bind random port on ssh host and forward to localhost

Might be useful for reverse shells. A simple replacement for `bore`.

```bash
RCKWRTZ_USAGE=$'\n\n    USAGE: rckwrtz username@host.com 1337'
RCKWRTZ_MISSING_LOCAL_PORT=$'Missing local port to remote forward.'$RCKWRTZ_USAGE
RCKWRTZ_MISSING_HOST=$'Missing ssh host to bind port on.'$RCKWRTZ_USAGE
function rckwrtz() {
  [ -z "$1" ] && ( echo $RCKWRTZ_MISSING_HOST; return 1 ) || host=$1
  [ -z "$2" ] && ( echo $RCKWRTZ_MISSING_LOCAL_PORT; return 1 )|| local_port=$2

  open_port=$(ssh $host -- 'ruby -rsocket -e "puts Addrinfo.tcp(\"\", 0).bind { |s| s.local_address.ip_port }"')
  echo "Opening port "${open_port}" on remote, plugging it to localhost:${local_port}..."
  ssh -N -R ${open_port}:\*:${local_port} $host
  echo "Forwarding. Press ctrl+c to abort."
}
```


### radare pwn pattern (debruijn sequence)

```bash
# find offset
ragg2 -P 512 -r | ./narnia1

# query 
ragg -q 0x41414841
```

### gdb (pwndbg) raw stdin input

```bash
# with python3
r < <(python3.9 -c 'import sys; sys.stdout.write("\x41"*50)')

# with python2
r < <(python2.7 -c 'print("\x41"*50)')

# with ruby
r < <(ruby -e 'print("A"*50)')
```

### print space without a space

```bash
python<<<'print("\x20")'

ruby<<<'print("\x20")'

{echo,-e,'\x20'}

{base64,-d}<<<IAo=

{echo,IAo=}|{base64,-d}

{xxd,-r,-p}<<<20

# $'\x20' will be interpreted as ' '
# <<< handles the string right of it, as a filestream
# zsh allows streaming, without program execution
zsh<<<"<<<$'\x20'>/dev/stdout"
zsh<<<"<<<$'\x20'>/proc/self/fd/1"

# use hex and octal
cat<<<$'\x20'
cat<<<$'\040'
```

### pwntools - enumerate bad and good chars

```python
import requests
from pwn import *

good_char, bad_char = ('', '')
with log.progress('Trying something...') as p:
    for c in range(0x20, 0x7f):
        url = 'http://challenge.nahamcon.com:30936/?echo=%%%02x'
        r = requests.get(url % c)
        p.status(url % c)
        char = chr(c)
        if "Hey mate, you seem to be using some characters" in r.text:
            bad_char = f'{bad_char}{char}'
        else:
            good_char = f'{good_char}{char}'
            log.info(chr(c))
print(f'Bad chars: {bad_char}')
print(f'Good char {good_char}')
```

### joern buildah 

```bash
c=$(buildah from docker.io/archlinux)
buildah run $c pacman --noconfirm -Syu
buildah run $c pacman --noconfirm -S jdk11-openjdk unzip gcc
buildah run $c curl -L "https://github.com/joernio/joern/releases/latest/download/joern-install.sh" -o joern-install.sh
buildah run $c chmod u+x joern-install.sh
buildah run $c ./joern-install.sh --interactive
buildah commit $c joern-arch
```
