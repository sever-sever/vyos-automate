
FROM alpine:3.19

RUN apk add --update nano gettext \
    && rm -rf /var/cache/apk/*

RUN mkdir -p /opt/gobgp/template

# Download and install gobgp
RUN wget https://github.com/osrg/gobgp/releases/download/v3.23.0/gobgp_3.23.0_linux_amd64.tar.gz -O /tmp/gobgp.tar.gz \
    && tar -zxf /tmp/gobgp.tar.gz --directory /tmp/ \
    && mv /tmp/gobgp /tmp/gobgpd /usr/local/bin/ \
    && rm -rf /tmp/*

# Copy the template file
COPY files/bgp.conf.template /opt/gobgp/template/bgp.conf.template

WORKDIR /opt/gobgp

# Create an entrypoint script
COPY files/entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

# Run the entrypoint script when the container starts
ENTRYPOINT ["/opt/entrypoint.sh"]

LABEL maintainer="Viachelav Hletenko"
