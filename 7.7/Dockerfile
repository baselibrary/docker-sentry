FROM baselibrary/python:2.7
MAINTAINER ShawnMa <qsma@thoughtworks.com>

## Version
ENV SENTRY_MAJOR   7.7
ENV SENTRY_RELEASE 7.7.4

## Dependencies
RUN \
  apt-get update && \
  apt-get install -y libpq-dev libmysqlclient-dev libxslt1-dev libxml2-dev libz-dev libffi-dev libssl-dev &&\
  rm -rf /var/lib/apt/lists/*

## Packages
RUN pip install --upgrade psycopg2 mysql-python python-decouple sentry==$SENTRY_RELEASE

## Configurations
ADD Procfile              /var/lib/sentry/Procfile
ADD config/sentry.conf.py /var/lib/sentry/sentry.conf.py
ADD config/crontab        /etc/crontab

## Environments
ENV SENTRY_CONF          /var/lib/sentry/sentry.conf.py
ENV SENTRY_DATA_DIR      /var/lib/sentry/data

## Scripts
ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x            /docker-entrypoint.sh

EXPOSE 9000

WORKDIR /var/lib/sentry

VOLUME ["${SENTRY_DATA_DIR}"]

ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]


