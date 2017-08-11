FROM alpine:3.6

# install dependencies
RUN apk add --update g++ libtool make automake curl autoconf supervisor python py-pip
RUN pip install requests

# copy files and create necessary folders
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY twemproxy.yaml /etc/twemproxy/conf/twemproxy.yaml

COPY run-twemproxy.sh /run-twemproxy.sh
COPY config-monitor.sh /config-monitor.sh
COPY create-config.py /create-config.py
COPY twemproxy.template /twemproxy.template

# compile twemproxy
RUN curl -qL https://github.com/twitter/twemproxy/archive/v0.4.1.tar.gz | tar xzf -
RUN cd  twemproxy-0.4.1 && autoreconf -fvi && ./configure --enable-debug=log && make && make install

RUN apk del g++ libtool make automake curl autoconf

EXPOSE 22121

CMD ["/config-monitor.sh", "/create-config.py"]
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
