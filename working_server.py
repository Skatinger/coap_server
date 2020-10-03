#!/usr/bin/env python3

import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
import datetime
from aiohttp import web


runners = []
async def start_site(app, port, address='0.0.0.0'):
    runner = web.AppRunner(app)
    runners.append(runner)
    await runner.setup()
    site = web.TCPSite(runner, address, port)
    await site.start()

async def index(request):
	return web.Response(text="hello from http server")

class CustomResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.set_content("ok, works---\n")

    def set_content(self, content):
        self.content = content

    async def render_get(self, request):
        print("woow, cool i received a GET request")
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('===== PUT payload: %s' % request.payload)
        self.set_content(request.payload.decode("utf-8") )
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

async def button_observe(request):
    print("BUTTON OBSERVE triggered with request:")
    print(request)
    return aiocoap.Message(payload="cool")

# logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

# setup http app
http_app = web.Application()
http_app.add_routes([web.get('/test', index)])
# http_app.add_routes([web.static('/', 'index.html')])
http_app.router.add_static('/', path='/app/static/', name='index')


# setup event loop for http
loop = asyncio.get_event_loop()
loop.create_task(start_site(http_app, port=8080))

# setup coap server
root = resource.Site()
root.add_resource(['.well-known', 'core'],
        resource.WKCResource(root.get_resources_as_linkheader))
root.add_resource(['testing'], CustomResource())
root.add_resource(['button_observe'], button_observe)
# creates a context to all addresses on the default coap port
asyncio.Task(aiocoap.Context.create_server_context(root))


try:
    loop.run_forever()
except:
    pass
finally:
    for runner in runners:
        loop.run_until_complete(runner.cleanup())
