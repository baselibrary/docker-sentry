FROM quay.io/baselibrary/python:2.7
MAINTAINER ShawnMa <qsma@thoughtworks.com>

## Install dependencies
RUN \
  apt-get update && \
  apt-get install -y libpq-dev libmysqlclient-dev libxslt1-dev libxml2-dev libz-dev libffi-dev libssl-dev &&\
  rm -rf /var/lib/apt/lists/*

## work dir 
WORKDIR /sentry

## Install apps
RUN pip install --upgrade redis hiredis nydus psycopg2 mysql-python python-memcached sentry==7.7.0

## Config apps
ADD Procfile             /sentry/Procfile
ADD files/sentry.conf.py /sentry/sentry.conf.py

## Config cron
ADD files/crontab        /etc/crontab

## Install scripts
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x            /docker-entrypoint.sh

EXPOSE 9000

VOLUME ["/sentry"]

ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]


