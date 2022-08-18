### forward wiregurad with socat

```bash
# try with bind first
socat udp-recvfrom:51871,reuseaddr,fork UDP:192.168.121.75:51871
```

### allow vpn host to forward packages

```bash
sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv6.conf.all.forwarding=1
```

### socat systemd unit

```bash
[Unit]
Description=udp bridge to wireguard vm

[Service]
Type=simple

ExecStart=socat udp-recvfrom:51871,reuseaddr,fork UDP:192.168.121.75:51871
Restart=always

[Install]
WantedBy=multi-user.target
```

### generate configs

```bash
function wg_keys() {
  [ -z "$1" ] && {
    echo "Missing filename prefix! Aborting..."
  }
  wg genkey | (umask 0077 && tee "$1.key") | wg pubkey > "$1.pub"
}

function wg_interface() {
  interface_priv_key="$1"
  interface_ip="$2"
  echo "[Interface]"
  echo "Address = ${interface_ip}/24"
  echo "ListenPort = 51871"
  echo "PrivateKey = ${interface_priv_key}"
}

function wg_masquerade() {
  echo "PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"
  echo "PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE"
}

function wg_config_peer_server() {
  peer_pub_key="$1"
  peer_ip="$2"
  echo "[Peer]"
  echo "PublicKey = $peer_pub_key"
  echo "AllowedIPs = $peer_ip/32"
}

function wg_config_peer_client() {
  peer_pub_key="$1"
  peer_ip="$2"
  echo "[Peer]"
  echo "PublicKey = $peer_pub_key"
  echo "AllowedIPs = $peer_ip/32, 13.37.0.0/24"
  echo "Endpoint = 192.168.122.105:51871"
}

# server
server_wireguard_name="swg0"
wg_keys "$server_wireguard_name"
wg_interface "$(cat ${server_wireguard_name}.key)" "13.37.1.1" > "${server_wireguard_name}.conf"
echo >> "${server_wireguard_name}.conf"
wg_masquerade >> "${server_wireguard_name}.conf"
echo >> "${server_wireguard_name}.conf"

mkdir -p participants
# clients
i=1
for p in $(cat participants.txt); do
  i=$((i+1))
  pushd participants
    wg_keys $p
    wg_interface   "$(cat $p.key)" "13.37.1.$i" > $p.conf
    echo >> $p.conf
    wg_config_peer_client "$(cat ../${server_wireguard_name}.pub)" "13.37.1.1"  >> $p.conf
    echo >> $p.conf
  popd
  echo "# $p" >> "${server_wireguard_name}.conf"
  wg_config_peer_server "$(cat participants/$p.pub)" "13.37.1.$i" >> "${server_wireguard_name}.conf"
  echo >> "${server_wireguard_name}.conf"
done
```
