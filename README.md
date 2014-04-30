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

client = forward.get_sshclient(bastionhost, pkey)
tunnel = forward.get_tunnel('windows.server', 4000, client)

```
