## CoAP Server and Thingy:91 Controller

#### Overview
This is a small server application which handles coap requests to collect data from a thingy:91 client.
Collected Data are air pressure, temperature and humidity.
It is also possible to change the color of the LED on the thingy. All data and actions
are available on a Website at `localhost:4100` once the app is started.

#### Details
##### CoAP implementation
Traffic between the thingy:91 and the server is implemented using the CoAP protocol. Payloads
are encoded in CBOR to reduce data size. Data points from the thingy:91 are sent periodically
to the server and stored in a MySQL database.  
The server also provides an observable resource *LED* which will be observed by the thingy:91.

##### Webpage
The webpage displays all collected data in charts. It will also show if the thingy:91 is online
and if so allows to change the color of the thingy:91 LED.


#### Setup
To run the application a mysql database is required. If docker-compose is available,
just run `docker-compose up` in the source directory and the db will start.

For the application itself, it can be run inside docker (uncomment in docker-compose.yml),
but some problems with udp ipv4 to udp ipv6 might occur. It is therefore advised
to run the app natively on a linux distro.

Run `pip3 install -r requirements.txt` to install all required libraries.
Then run `python server.py` to start the application. The Website can be found on
 `localhost:4100`.
