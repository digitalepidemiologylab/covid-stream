FROM python:3.6
MAINTAINER Martin Müller "martin.muller@epfl.ch"

# Install python dependencies
COPY ./requirements.txt /home/app/requirements.txt
WORKDIR /home/app
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy files
COPY . /home/app
VOLUME ["/home/app"]
