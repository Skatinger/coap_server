#!/usr/bin/env python3

import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiohttp_cors
import aiocoap
import datetime
import aiomysql
import json
import random
from aiohttp import web
import database



# connects to db, saves a connector the the app dict
async def init_db(app):
    connection = await aiomysql.connect(
        host='db',
        user='root',
        password='1324',
        db='db')
    if connection:
        print("got db connection:" + str(connection))
    app['db'] = connection

async def setup_db(app):
    conn = app['db']
    cur = await conn.cursor()
    try:
        queries = []
        queries.append('''CREATE TABLE `temperature` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `celcius` float DEFAULT NULL,
          `time` datetime DEFAULT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')
        # queries.append('''CREATE TABLE `humidity` (
        #   `id` int(11) NOT NULL AUTO_INCREMENT,
        #   `celcius` float DEFAULT NULL,
        #   `time` datetime DEFAULT NULL,
        #   PRIMARY KEY (`id`)
        # ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')
        # queries.append('''CREATE TABLE `temperature` (
        #   `id` int(11) NOT NULL AUTO_INCREMENT,
        #   `celcius` float DEFAULT NULL,
        #   `time` datetime DEFAULT NULL,
        #   PRIMARY KEY (`id`)
        # ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')
        # queries.append('''CREATE TABLE `temperature` (
        #   `id` int(11) NOT NULL AUTO_INCREMENT,
        #   `celcius` float DEFAULT NULL,
        #   `time` datetime DEFAULT NULL,
        #   PRIMARY KEY (`id`)
        # ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')
        # queries.append('''CREATE TABLE `temperature` (
        #   `id` int(11) NOT NULL AUTO_INCREMENT,
        #   `celcius` float DEFAULT NULL,
        #   `time` datetime DEFAULT NULL,
        #   PRIMARY KEY (`id`)
        # ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')


        for query in queries:
            await cur.execute(query)
        await self.connector.commit()
        await cur.close()
    except:
        return

runners = []
async def start_site(app, port, address='0.0.0.0'):
    runner = web.AppRunner(app)
    runners.append(runner)
    await runner.setup()
    site = web.TCPSite(runner, address, port)
    await site.start()

# returns static file with a websocket to poll data / send data
async def index(request):
    return web.FileResponse('./static/index.html')

async def update_led(request):
    # todo parse hex color, then notify LED
    color = request.match_info.get('hexcolor')
    print("GOT COLOR: " + color)
    if(len(color) != 6):
      return
    LedResource().update_resource(color)
    # LedResource().notify()
    return web.json_response({'color': color})

async def get_measurment(request):
    type = request.match_info.get('measurement')
    conn = request.app['db']
    data = await database.DBConnector(conn).fetchall(type)
    print(data)
    return web.json_response(data)


# COAP SERVER =============================================
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
        # self.update_resource("")
        self.updated_state()
        # self.reschedule()

    def update_resource(self, color):
        # if(len(color) == 0):
            # colors = ["ff0000", "ebe134", "abcdef", "ffffff", "gggggg"]
            # self.color = random.choice(colors)
        # else:
        self.color = color
        self.notify()

    # during testing we call this, once the server runs we send messages from http_app
    # to trigger a notify instead of calling it here
    # def reschedule(self):
        # self.handle = asyncio.get_event_loop().call_later(5, self.notify)

    # def update_observation_count(self, count):
    #     if count and self.handle is None:
    #         self.reschedule()


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


# Configure default CORS settings.
cors = aiohttp_cors.setup(http_app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*",
        )
})

cors.add(http_app.router.add_get('/', index))
cors.add(http_app.router.add_get('/update_led/{hexcolor}', update_led))
cors.add(http_app.router.add_get('/{measurement}', get_measurment))


# setup event loop for http
loop = asyncio.get_event_loop()
loop.run_until_complete(init_db(http_app))
loop.run_until_complete(setup_db(http_app))



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

# database_setup(http_app)

try:
    loop.run_forever()
except:
    pass
finally:
    for runner in runners:
        loop.run_until_complete(runner.cleanup())
