### create pub and private key

```bash
function wg_keys() {
  [ -z "$1" ] && { 
    echo "Missing filename prefix! Aborting..."
  }
  wg genkey | (umask 0077 && tee "$1.key") | wg pubkey > "$1.pub"
}
```

### forward with socat

```bash
# try with bind first
socat udp-recvfrom:51871,reuseaddr,bind=192.168.121.75,fork UDP:192.168.121.75:51871
```
