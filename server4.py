import asyncio

async def handle_echo(request):
    web.Response("helllooo")

# Start server 1
coro1 = asyncio.start_server(handle_echo, '127.0.0.1', 8080, loop=loop)
server1 = loop.run_until_complete(coro1)
print('Serving 1 on {}'.format(server1.sockets[0].getsockname()))

# Start server 2
coro2 = asyncio.start_server(handle_echo, '127.0.0.1', 8081, loop=loop)
server2 = loop.run_until_complete(coro2)
print('Serving 2 on {}'.format(server2.sockets[0].getsockname()))

# Serve requests until Ctrl+C is pressed
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the servers
server1.close()
loop.run_until_complete(server1.wait_closed())
server2.close()
loop.run_until_complete(server2.wait_closed())

# Close the loop
loop.close()
