import sys

import eventlet

import tunnel


client = tunnel.get_sshclient('bastion.server', username='bastion.user', password='pa$$')
tunnel = tunnel.connect('123.45.67.89', 445, client)
tunnel.serve_forever()
print "tunnel is running on %s !" % tunnel.address

if len(sys.argv) > 1:
    n = sys.argv[1]
else:
    n = 50

for x in range(n):
    sys.stdout.write('.')
    sys.stdout.flush()
    eventlet.sleep(1)

