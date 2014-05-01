import sys

from pse import PSE


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print "run.py <localport> <command>"
        sys.exit()

    port = sys.argv[1]
    command = " ".join(sys.argv[1:])

    pse_client = PSE(host='localhost', port=port, username="Administrator", password="p@ssw0rd")
    pse_client.connect()
    pse_client.execute('echo hello')  # windows command
