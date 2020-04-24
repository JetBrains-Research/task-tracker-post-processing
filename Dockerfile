# Use the official image as a parent image
FROM python:3.7

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
# Install gcc
RUN apt-get install -y gcc
# Install JRE
RUN apt-get install -y default-jre
# Install JDK
RUN apt-get install -y default-jdk
# Install kotlin
# Todo: install kotlin with snap
# See: https://stackoverflow.com/questions/58385340/dockerfile-how-install-snap-snapd-unrecognized-service
# See: https://github.com/ogra1/snapd-docker
#RUN apt install -y snapd
#RUN snap install --classic kotlin

# Copy the file from your host to your current location
# And run the command inside your image filesystem
WORKDIR /opt
COPY requirements.txt /opt/requirements.txt
RUN pip3 install -r requirements.txt

COPY dev-requirements.txt /opt/dev-requirements.txt
RUN pip3 install -r dev-requirements.txt

COPY test-requirements.txt /opt/test-requirements.txt
RUN pip3 install -r test-requirements.txt

COPY gumtree-2.1.2.zip /opt/gumtree-2.1.2.zip
RUN unzip gumtree-2.1.2.zip
#	&& ln -s /opt/gumtree-2.1.2/bin/gumtree /usr/bin/gumtree
