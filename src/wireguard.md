### create pub and private key

```bash
function wg_keys() {
  [ -z "$1" ] && { 
    echo "Missing filename prefix! Aborting..."
  }
  wg genkey | (umask 0077 && tee "$1.key") | wg pubkey > "$1.pub"
}
```
