tunnels
=======

ssh tunnels with paramiko


#### usage

```bash
pip install -r requirements.txt
```

```python
import forward

client = forward.get_sshclient()
tunnel = forward.get_tunnel(client)

```
