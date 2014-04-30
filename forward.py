import os
import socket
import select
try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

from satori import ssh


class ForwardServer (SocketServer.ThreadingTCPServer):
    daemon_threads = True
    # I doubt we want this to be True ???
    allow_reuse_address = True


class Handler (SocketServer.BaseRequestHandler):

    def handle(self):
        try:
            chan = self.ssh_transport.open_channel('direct-tcpip',
                                                   (self.chain_host, self.chain_port),
                                                   self.request.getpeername())
        except Exception as e:
            print ('Incoming request to %s:%d failed: %s' % (self.chain_host,
                                                              self.chain_port,
                                                              repr(e)))
            return
        if chan is None:
            print ('Incoming request to %s:%d was rejected by the SSH server.' %
                   (self.chain_host, self.chain_port))
            return

        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)

        peername = self.request.getpeername()
        chan.close()
        self.request.close()
        print 'Tunnel closed from %r' % peername


class Tunnel(object):

    def __init__(self, remote_host, remote_port,
                 bastionclient, local_port=0):

        # Nico,
        # perhaps this class (or this module) should be the one who handles which
        # local_port is bound to this tunnel (hence local_port=None),
        # that way the end instantiating the
        # class instance can look to see where its running...
        # this would assume that the user of this class doesnt actually care
        # which port the Tunnel ends up on and that this class would handle any
        # attempts to bind to a port that's already being used

        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_port = local_port
        self.bastionclient = bastionclient

        self._tunnel = None
        self._tunnel_thread = None

    def serve(self):
        self._ssh_transport = self.bastionclient.get_transport()

        # this is gross

        #############################################
        # this is a little convoluted, but lets me configure things for the Handler
        # object.  (SocketServer doesn't give Handlers any way to access the outer
        # server normally.)
        #############################################

        class SubHandler(Handler):
            chain_host = self.remote_host
            chain_port = self.remote_port
            ssh_transport = self._ssh_transport

        self._tunnel = ForwardServer(('localhost', self.local_port), SubHandler)
        # TODO:
        # implement async that Nico is working on for this call

    def serve_forever(self, block=True):
        if block:
            self._tunnel.serve_forever()
        threading.Thread(self._tunnel.serve_forever).start()

    def shutdown(self):

        self._tunnel.shutdown()


HELP = """\
Set up a forward tunnel across an SSH server, using paramiko. A local port
(given with -p) is forwarded across an SSH session to an address:port from
the SSH server. This is similar to the openssh -L option.
"""


def get_tunnel(targethost, targetport, sshclient):

    # reasons to use satori's modified version of paramiko.SSHClient
    #   1) hackishly tries to respond to password prompts
    #   2) responds to demands for a TTY by reconnecting with a pseudo tty
    #   3) prioritizes authentication mechanisms

    # TODO: change this to satori.ssh and give some thought to bash.RemoteClient
    return Tunnel(targethost, targetport, sshclient)


def get_sshclient(bastionhost, pkeystring=None, username="lnx-waldo"):

    client = ssh.connect(bastionhost, username=username,
                         private_key=pkeystring,
                         options={'StrictHostKeyChecking': False})

    return client

