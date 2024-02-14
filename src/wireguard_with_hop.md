# Route all traffic through a hop node
Sometimes you want to route all your traffic through a wireguard gateway. But,
you also want to add a node to hop over. So in total there are three systems:

  - A `peer` which routes all traffic over the `hop` to the `gateway`.
  - A `hop` node which is accessible to both systems, it's accessible for both
    systems. 
  - A `gateway` which is behind a NATed network and therefore can not be
    accessed directly through the net. The `gateway` has to keep the connection
    alive to the `hop`, because the NATed gateway might prohibit the `hop` to send
    packages after a while.

All these nodes have their own wireguard configs, so their own private key and
public key.

For the hop node, make sure to use policy based routing. This can be done mixed
with `PreUp` hooks triggering ip rules which are the policies. Also, a `Table`
can be specified for the interface. The routing rules are specified through
the `Peer` sections. So all traffic from the wireguard interface is routed only
on that interface. The configuration file for the `hop` looks as follows:

```
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <hop privkey>
Table = 123
PreUp = sysctl -w net.ipv4.ip_forward=1
PreUp = ip rule add iif %i table 123 priority 456
PostDown = ip rule del iif %i table 123 priority 456

# a simple peer
[Peer]
PublicKey = <peer pubkey>
AllowedIPs = 10.0.0.3/32

# gateway, all traffic of the 123 table is routed to this.
[Peer]
PublicKey = <gateway pubkey>
AllowedIPs = 0.0.0.0/0
```

After setting up the `hop` node, you can proceed with the `gateway` node. The
`gateway` node also uses hooks for additional system configuration. But instead
of adjusting rules for policy based routing, network packages are NAT'ed using
`iptables`. The keyword here is `maqsquerade`. Additionally, the `gateway`
itself might sit behind a NAT (e.g. a home router). To work around that NAT and
therefore allow the `hop` node to initate communication to the `gateway` node,
a persistent keep alive is configured. You might have to adjust the output
interface (`wlan0`) in the masquerading to your suited output inteface (e.g.
`eth0` or `en1`).

```
[Interface]
Address = 10.0.0.2/24
ListenPort = 51820
PrivateKey = <gateway privkey>
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o wlan0 -j MASQUERADE

[Peer]
PublicKey = <hop pub>
AllowedIPs = 10.0.0.1/32, 10.0.0.3/32
Endpoint = 23.88.55.78:51820
PersistentKeepalive = 25
```

As the last configuration file, the peer follows. The endpoint specification of
`0.0.0.0/0`, causes all traffic to be routed to that client. An DNS server must be
specified.

```
[Interface]
Address = 10.0.0.3/24
ListenPort = 51820
PrivateKey = <peer privkey>
# adjust the dns server to the local dns server onsite
DNS = 1.1.1.1

[Peer]
PublicKey = <hop pubkey>
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = 23.88.55.78:51820
```
