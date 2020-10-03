import asyncio
from aiohttp import web

runners = []
# creates web app as a runner
async def start_site(app, port, address='0.0.0.0'):
    runner = web.AppRunner(app)
    runners.append(runner)
    await runner.setup()
    site = web.TCPSite(runner, address, port)
    await site.start()

# http apps ===========
async def index(request):
    return web.Response(text='helllooooo')

async def index2(request):
    return web.Response(text='this is a test')

http_app = web.Application()
http_app.add_routes([web.get('/', index)])
http2_app = web.Application()
http2_app.add_routes([web.get('/', index2)])

# setup event loop
loop = asyncio.get_event_loop()
loop.create_task(start_site(http_app, port=8080))
loop.create_task(start_site(http2_app, port=8081))

try:
    loop.run_forever()
except:
    pass
finally:
    for runner in runners:
        loop.run_until_complete(runner.cleanup())
