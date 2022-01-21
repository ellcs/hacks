
# restrict keyforwarding

https://www.openssh.com/agent-restrict.html

```bash
$ ssh-add -h "perseus@cetus.example.org" \
          -h "scylla.example.org" \
          -h "scylla.example.org>medea@charybdis.example.org" \
          ~/.ssh/id_ed25519
```
