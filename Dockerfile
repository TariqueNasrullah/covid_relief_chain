FROM ubuntu

RUN apt-get update -y
RUN apt-get install apt-utils -y
RUN apt-get install python3.7 -y
RUN ln -s python3.7 /usr/bin/python3
RUN apt-get install python3-pip -y

ENV PYTHONBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt
COPY . /code/