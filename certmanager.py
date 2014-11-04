import random
import sys
from OpenSSL import crypto

def create_root_ca():
    pkey = crypto.PKey()
    pkey.generate_key(crypto.TYPE_RSA, 4096)

    cert = crypto.X509()
    cert.set_version(3)
    cert.set_serial_number(int(random.random() * sys.maxsize))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(60 * 60 * 24 * 365)

    subject = cert.get_subject()
    subject.CN = "example.com"
    subject.O = "mycommonname"

    issuer = cert.get_issuer()
    issuer.CN = "example.com"
    issuer.O = "mycommonname"

    cert.set_pubkey(pkey)
    cert.add_extensions([
        crypto.X509Extension(b"basicConstraints", True,
                             b"CA:TRUE"),
        crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash",
                             subject=cert)
    ])
    cert.add_extensions([
        crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid:always",
            issuer=cert)
    ])
    cert.sign(pkey, "sha1")

    with open("root.pem", "wb") as certfile:
        certfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        certfile.close()

    with open("root.key", "wb") as pkeyfile:
        pkeyfile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
        pkeyfile.close()

def create_certificate(cn, o, serverside, certfilename, pkeyfilename):
    rootpem = open("root.pem", "rb").read()
    rootkey = open("root.key", "rb").read()
    ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, rootpem)
    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, rootkey)

    pkey = crypto.PKey()
    pkey.generate_key(crypto.TYPE_RSA, 2048)

    cert = crypto.X509()
    cert.set_serial_number(int(random.random() * sys.maxsize))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(60 * 60 * 24 * 365)
    cert.set_version(3)

    subject = cert.get_subject()
    subject.CN = cn
    subject.O = o

    if serverside:
        cert.add_extensions([crypto.X509Extension(b"subjectAltName", False,
            b"DNS:test1.example.com,DNS:test2.example.com")])

    cert.set_issuer(ca_cert.get_subject())

    cert.set_pubkey(pkey)
    cert.sign(ca_key, "sha1")


    with open(certfilename, "wb") as certfile:
        certfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        certfile.close()

    with open(pkeyfilename, "wb") as pkeyfile:
        pkeyfile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
        pkeyfile.close()


print("Making root CA")
create_root_ca()
print("Making server certificate")
create_certificate("server", "my organisation", True, "server.crt", "server.key")
print("Making client certificate")
create_certificate("client", "my organisation", False, "client.crt", "client.key")
