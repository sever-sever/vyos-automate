
FROM alpine

RUN apk add --update nano \
    && rm -rf /var/cache/apk/*

RUN mkdir /opt/gobgp

WORKDIR /opt/gobgp

RUN wget https://github.com/osrg/gobgp/releases/download/v3.21.0/gobgp_3.21.0_linux_amd64.tar.gz -O /tmp/gobgp.tar.gz \
    && tar -zxf /tmp/gobgp.tar.gz --directory /tmp/ \
    && mv /tmp/gobgp /tmp/gobgpd /usr/local/bin/ \
    && rm -rf /tmp/*

CMD gobgpd --config-file=/opt/gobgp/bgp.conf
