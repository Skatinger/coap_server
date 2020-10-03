#!/usr/bin/env python3

import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
# from influxdb import InfluxDBClient
import datetime
from aiohttp import web

# value is shared between IRC and the web server.
value = None



# class CustomResource(resource.Resource):
#     def __init__(self):
#         super().__init__()
#         self.set_content("ok, works---\n")
#
#     def set_content(self, content):
#         self.content = content
#
#     async def render_get(self, request):
#         print("woow, cool i received a GET request")
#         return aiocoap.Message(payload=self.content)
#
#     async def render_put(self, request):
#         print('===== PUT payload: %s' % request.payload)
#         # saveToInflux("esp8266", "temperature", request.payload)
#         # have to decode the payload as it is sent as bytestring
#         self.set_content(request.payload.decode("utf-8") )
#         return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)


# logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

# async def irc_server():
#     global value
#     async with irc_connect('irc.freenode.net#python-fr') as irc:
#         async for message in irc:
#             # if message is echo, reply with the current value
#             # otherwise store the message as value
#             if message == 'echo':
#                 irc.send(value)
#             else:
#                 value = message

# async def web_server():
#     global value

    # async with web_connect('localhost:8080') as web:
    #     async for request in web:
    #         if request.path == 'echo':
    #             request.client.send(value)
    #         else:
    #             value = request.path  # this is silly but simple

print("creating loop")
# web_server()


# async def index(request):
#     return web.Response(text="hello world")
async def web_server():
    app = web.Application()
    # app.add_routes([web.get('/', hello)])
    web.run_app(app)


loop = asyncio.get_event_loop()
loop.create_task(web_server())
# loop.create_task(irc_server())

loop.run_forever()

# def main():
#     # Resource tree creation
#     root = resource.Site()
#
#     root.add_resource(['.well-known', 'core'],
#             resource.WKCResource(root.get_resources_as_linkheader))
#     # root.add_resource(['time'], TimeResource())
#     # root.add_resource(['other', 'block'], BlockResource())
#     root.add_resource(['testing'], CustomResource())
#     # root.add_resource(['other', 'separate'], SeparateLargeResource())
#
#     # creates a context to all addresses on the default coap port
#     asyncio.Task(aiocoap.Context.create_server_context(root))
#
#     asyncio.get_event_loop().run_forever()
#
# if __name__ == "__main__":
#     # initialize client
#     client = InfluxDBClient(host='localhost', port=8086)
#     if client:
#         print("got database connection")
#         print(client)
#     else:
#         print("no database connection, records will not be saved.")
#
#     main()
