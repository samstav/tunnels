tunnels
=======

ssh tunnels with paramiko


### as a psexec proxy
```bash
pip install -r requirements.txt
```

```python
import tunnel

bastionhost = 'my.bastion'
pkey = open('~/.ssh/id_rsa', 'r').read()

client = tunnel.get_sshclient(bastionhost, private_key=pkey)
tunnel = tunnel.connect('windows.server', 445, client)

# what port was my tunnel assigned? (defaults to localhost:P)
print tunnel.address
... ('127.0.0.1', 59277)

tunnel.serve_forever()

# not yet implemented
c2 = tunnel.get_psexecclient('localhost', 59277)
c2.remote_execute('echo hello')

```

### as an ssh proxy
```python
bastionhost = 'my.bastion'
pkey = open('~/.ssh/id_rsa', 'r').read()

client = tunnel.get_sshclient(bastionhost, private_key=pkey)
tunnel = tunnel.connect('linux.server', 22, client)

# what port was my tunnel assigned? (defaults to localhost:P)
print tunnel.address
... ('127.0.0.1', 59268)
tunnel.serve_forever()

c2 = tunnel.get_sshclient('localhost', 59268)
c2.remote_execute('echo hello')
```
