tunnels
=======

ssh tunnels with paramiko


### usage
```bash
pip install -r requirements.txt
```

```python
import forward

bastionhost = 'my.bastion'
pkey = open('~/.ssh/id_rsa', 'r').read()

client = forward.get_sshclient(bastionhost, private_key=pkey)
tunnel = forward.get_tunnel('windows.server', 445, client)

# what port was my tunnel assigned? (defaults to localhost:P)
print tunnel.tunnel_address
tunnel.serve_forever(async=True)

```
