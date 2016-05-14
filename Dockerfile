FROM python:2.7.11-slim
MAINTAINER Daria Shubina <daria.shubina@gmail.com>

RUN apt-get update && apt-get install -qq -y \
    build-essential \
    libpq-dev \
    postgresql-client-9.4 \
    nodejs \
    npm \
    --fix-missing --no-install-recommends

ENV INSTALL_PATH /crashatmypad
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install
RUN npm install -g gulp
RUN gulp build

CMD gunicorn -b 0.0.0.0:8000 "crashatmypad.app:create_app()"
