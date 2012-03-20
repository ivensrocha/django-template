import socket

if socket.gethostname() == "my-server":
    DEPLOY = True
    from settings_deploy import *
else:
    DEPLOY = False
    from settings_dev import *
