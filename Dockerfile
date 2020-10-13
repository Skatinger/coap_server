FROM python:3.7

ENV APP_HOME /app

# RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ADD ./ $APP_HOME/

RUN apt-get update
RUN apt-get install nano

RUN pip3 install aiohttp aiocoap aiohttp-cors aiomysql
