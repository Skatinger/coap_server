#!/usr/bin/env python3

import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
import datetime
import json
import random
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

    # async def render_get(self, request):
    #     print("woow, cool i received a GET request")
    #     return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('===== PUT payload: %s' % request.payload.decode("utf-8"))
        self.set_content( request.payload.decode("utf-8") )
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)


class LedResource(resource.ObservableResource):
    """Example resource that can be observed. The `notify` method keeps
    scheduling itself, and calles `update_state` to trigger sending
    notifications."""

    def __init__(self):
        super().__init__()

        self.handle = None
        self.color = "ffffff"

    def notify(self):
        self.update_resource()
        self.updated_state()
        self.reschedule()

    def update_resource(self):
        colors = ["ff0000", "ebe134", "abcdef", "ffffff", "gggggg"]
        self.color = random.choice(colors)

    # during testing we call this, once the server runs we send messages from http_app
    # to trigger a notify instead of calling it here
    def reschedule(self):
        self.handle = asyncio.get_event_loop().call_later(5, self.notify)

    def update_observation_count(self, count):
        if count and self.handle is None:
            self.reschedule()


    async def render_get(self, request):
        print("COLOR IS:")
        print("sdfasdfasdf" + self.color)
        payload = ("{\"appId\":\"LED\",\"data\":{\"color\":\"" + self.color + "\"},\"messageType\":\"CFG_SET\"}").encode("utf-8")
        return aiocoap.Message(payload=payload)

# used for testing, works
class TimeResource(resource.ObservableResource):
    """Example resource that can be observed. The `notify` method keeps
    scheduling itself, and calles `update_state` to trigger sending
    notifications."""

    def __init__(self):
        super().__init__()

        self.handle = None

    def notify(self):
        self.updated_state()
        self.reschedule()

    def reschedule(self):
        self.handle = asyncio.get_event_loop().call_later(5, self.notify)

    def update_observation_count(self, count):
        if count and self.handle is None:
            print("Starting the clock")
            self.reschedule()
        if count == 0 and self.handle:
            print("Stopping the clock")
            self.handle.cancel()
            self.handle = None

    async def render_get(self, request):
        payload = datetime.datetime.now().\
                strftime("%Y-%m-%d %H:%M").encode('ascii')
        return aiocoap.Message(payload=payload)

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
root.add_resource(['led'], LedResource())
root.add_resource(['time'], TimeResource())

# creates a context to all addresses on the default coap port
asyncio.Task(aiocoap.Context.create_server_context(root))


try:
    loop.run_forever()
except:
    pass
finally:
    for runner in runners:
        loop.run_until_complete(runner.cleanup())
