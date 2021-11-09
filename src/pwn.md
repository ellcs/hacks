
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
