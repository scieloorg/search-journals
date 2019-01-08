FROM tomcat

ADD ./docker/tomcat/iahx-controller.war /usr/local/tomcat/webapps/

RUN unzip /usr/local/tomcat/webapps/iahx-controller.war -d /usr/local/tomcat/webapps/iahx-controller

RUN sed -ie 's/default=localhost:8981/default=solr:8983/g' /usr/local/tomcat/webapps/iahx-controller/WEB-INF/classes/controller.properties

CMD ["catalina.sh", "run"]