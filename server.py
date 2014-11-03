import asyncio
import ssl


@asyncio.coroutine
def client_connected(reader, writer):
    print(writer.get_extra_info("socket").getpeercert())
    writer.write(b"hai there ^_^\n")
    writer.close()


sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
sslcontext.verify_mode = ssl.CERT_REQUIRED
sslcontext.load_cert_chain(certfile="server.crt", keyfile="server.key")
sslcontext.load_verify_locations("root.pem")

print(sslcontext.cert_store_stats())
loop = asyncio.get_event_loop()
asyncio.async(asyncio.start_server(client_connected, "127.0.0.1", 1234, ssl=sslcontext))

loop.run_forever()
