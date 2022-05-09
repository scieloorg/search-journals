# Build static files container
FROM node:10.15.3 AS buildstatic

COPY . /app
WORKDIR /app

RUN npm install -y
RUN npm install -g gulp-cli

RUN cd /app \
    && gulp

FROM ubuntu:14.04

MAINTAINER Jamil Atta Junior<atta.jamil@gmail.com>

RUN apt-get update
RUN apt-get -y upgrade

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install apache2 libapache2-mod-php5 php5-mysql php5-gd php5-mcrypt php5-curl php5-redis php5-memcached curl lynx-cur python-setuptools collectd vim python-pip supervisor

# Enable apache mods.
RUN a2enmod php5
RUN a2enmod rewrite
RUN a2enmod remoteip

RUN sed -ie 's/memory_limit\ =\ 128M/memory_limit\ =\ 2G/g' /etc/php5/apache2/php.ini
RUN sed -i 's/\;date\.timezone\ =/date\.timezone\ =\ America\/Sao_Paulo/g' /etc/php5/apache2/php.ini
RUN sed -ie 's/upload_max_filesize\ =\ 2M/upload_max_filesize\ =\ 200M/g' /etc/php5/apache2/php.ini
RUN sed -ie 's/post_max_size\ =\ 8M/post_max_size\ =\ 200M/g' /etc/php5/apache2/php.ini

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

EXPOSE 80

# Copy site into place.
ADD iahx /var/www/iahx
ADD iahx-sites/scieloorg /var/www/iahx-sites/scieloorg
ADD iahx-sites/revenf /var/www/iahx-sites/revenf

# Work place.
WORKDIR /var/www/iahx

# Copy static(s)
COPY --from=buildstatic /app/iahx/static/ /var/www/iahx/static/
COPY --from=buildstatic /app/iahx-sites/revenf/static/ /var/www/iahx-sites/revenf/static/
COPY --from=buildstatic /app/iahx-sites/scieloorg/static/ /var/www/iahx-sites/scieloorg/static/

RUN mv config/config-mail-TEMPLATE.php config/config-mail.php

RUN mkdir -p /var/www/iahx-sites/scieloorg/logs
RUN mkdir -p /var/www/iahx-sites/revenf/logs

RUN chown -R www-data:www-data /var/www/iahx-sites/scieloorg/logs
RUN chown -R www-data:www-data /var/www/iahx-sites/revenf/logs

# Update the default apache site with the config we created.
ADD config/apache/apache-config.conf /etc/apache2/sites-enabled/000-default.conf
ADD config/apache/foreground.sh /etc/apache2/foreground.sh
ADD config/apache/mpm_prefork.conf /etc/apache2/mods-available/mpm_prefork.conf

# Enable mod_expires
RUN cp /etc/apache2/mods-available/expires.load /etc/apache2/mods-enabled/

# supervisord config
ADD config/supervisor/supervisord.conf /etc/supervisord.conf

RUN chmod 755 /etc/apache2/foreground.sh
RUN mkdir -p /var/log/supervisor/

# By default, run start.sh script
CMD ["supervisord", "-n", "-c", "/etc/supervisord.conf"]
