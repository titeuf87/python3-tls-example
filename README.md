python3-tls-example
===================
This is an example on how to use TLS together with python 3 and asyncio.

Creation of the certifications require pyopenssl. But the client and the server don't require it and works with just the builtin modules in python.

Files
=====
`certmanager.py`
This script is used to create the various certificates.
It first create the root CA certificate. And then two other certificates: one for the server and another for the client, both signed by the root CA.

`server.py`
Example of a server, listens to port 1234 by default.
The server requires the client to provide a certificate and once connected this certificate gets displayed.

`client.py`
Example of a client that both checks that the server certificate is valid and that provides a certificate to the server for authentication.


check_hostname
==============
The client explicitly sets `check_hostname` to `False`. When deploying this it's a good idea to enable this so that the client checks the hostname is valid with the server certificate.

For this the server certificate needs to be changed to include the actual hostname (either in the CN or as an alternative name). When the client connects it will check this and abort should the hostname not match.
