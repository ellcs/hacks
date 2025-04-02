
### punch a hole into nftables

```bash
# insert it, don't use `add`
nft insert rule inet filter INPUT tcp dport 2022 accept

# list all rules
nft list ruleset
```
