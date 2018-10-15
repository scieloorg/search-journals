FROM ubuntu:14.04

MAINTAINER Jamil Atta Junior<atta.jamil@gmail.com>

RUN apt-get update
RUN apt-get -y upgrade

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install apache2 libapache2-mod-php5 php5-mysql php5-gd php5-mcrypt php5-curl php5-redis php5-memcached curl lynx-cur python-setuptools collectd vim python-pip

# Install supervisord
RUN pip install supervisor

# Enable apache mods.
RUN a2enmod php5
RUN a2enmod rewrite

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
ADD iahx /var/www/site

# Work place.
WORKDIR /var/www/site

RUN mv config/config-mail-TEMPLATE.php config/config-mail.php

RUN chown -R www-data:www-data /var/www/site/logs

# Update the default apache site with the config we created.
ADD config/apache/apache-config.conf /etc/apache2/sites-enabled/000-default.conf
ADD config/apache/foreground.sh /etc/apache2/foreground.sh

# Enable mod_expires
RUN cp /etc/apache2/mods-available/expires.load /etc/apache2/mods-enabled/

# supervisord config
ADD config/supervisor/supervisord.conf /etc/supervisord.conf

RUN chmod 755 /etc/apache2/foreground.sh
RUN mkdir /var/log/supervisor/

# By default, run start.sh script
CMD ["supervisord", "-n", "-c", "/etc/supervisord.conf"]
