
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

