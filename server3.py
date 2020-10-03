import asyncio
from aiohttp import web
import aiocoap.resource as resource
import aiocoap

runners = []

async def start_site(app, address='0.0.0.0', port=8080):
    runner = web.AppRunner(app)
    runners.append(runner)
    await runner.setup()
    site = web.TCPSite(runner, address, port)
    await site.start()



# http app ===========
async def index(request):
    return web.Response(text='helllooooo')

http_app = web.Application()
http_app.add_routes([web.get('/', index)])


# coap app ==============
# class CustomResource(resource.Resource):
#     def __init__(self):
#         super().__init__()
#
#     def set_content(self, content):
#         self.content = content
#
#     async def render_get(self, request):
#         return aiocoap.Message(payload=self.content)
#
#     async def render_put(self, request):
#         print('===== PUT payload: %s' % request.payload)
#         self.set_content(request.payload.decode("utf-8") )
#         return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

root = resource.Site()
root.add_resource(['.well-known', 'core'],
        resource.WKCResource(root.get_resources_as_linkheader))
root.add_resource(['testing'], CustomResource())
asyncio.Task(aiocoap.Context.create_server_context(root))

# asyncio.get_event_loop().run_forever()



# ==== initialize apps ==================
loop = asyncio.get_event_loop()

loop.create_task(start_site(http_app, port=8080))
loop.create_task(start_site(web.Application(), port=8081))

try:
    loop.run_forever()
except:
    pass
finally:
    for runner in runners:
        loop.run_until_complete(runner.cleanup())
