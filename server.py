#!/usr/bin/env python3

import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
# from influxdb import InfluxDBClient
import datetime


# def saveToInflux(device, sensor, measurement):
#     print("Saving new record to db")
#     output_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
#     print(output_date)
#     client.switch_database('pyexample')
#     print("=========")
#     print(measurement.decode("ascii"))
#     # print("SAVE QUERY:")
#     # print([
#     #     {"measurement": "test_temperature", "tags": {"room": "room1", "id": "6"},
#     #     "time": output_date, #"2020-05-12T8:09:00Z",
#     #      "fields": { "temperature": measurement.decode("ascii")}}])
#
#     client.write_points([
#         {"measurement": "room_temperature",
#         "tags": {"room": "house"},
#         "time": output_date, #"2020-05-12T8:09:00Z",
#          "fields": { "temperature": 44}}]) #measurement.decode("ascii")}}])


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
        # saveToInflux("esp8266", "temperature", request.payload)
        # have to decode the payload as it is sent as bytestring
        self.set_content(request.payload.decode("utf-8") )
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

# logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(['.well-known', 'core'],
            resource.WKCResource(root.get_resources_as_linkheader))
    # root.add_resource(['time'], TimeResource())
    # root.add_resource(['other', 'block'], BlockResource())
    root.add_resource(['testing'], CustomResource())
    # root.add_resource(['other', 'separate'], SeparateLargeResource())

    # creates a context to all addresses on the default coap port
    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    # # initialize client
    # client = InfluxDBClient(host='localhost', port=8086)
    # if client:
    #     print("got database connection")
    #     print(client)
    # else:
    #     print("no database connection, records will not be saved.")

    main()
