FROM python:3.9-alpine

RUN mkdir -p /opt/web/logs /opt/web/uploads
WORKDIR /opt/web/app

COPY ./web/ /opt/web/listener/
COPY ./docker-entrypoint.sh /opt/gctf/listener/docker-entrypoint.sh
COPY ./requirements.txt /opt/web/listener   /requirements.txt

RUN chmod +x /opt/web/listener/docker-entrypoint.sh
RUN pip install --upgrade pip && \
    pip install -r /opt/web/listener/requirements.txt

ENTRYPOINT ["/opt/web/app/docker-entrypoint.sh"]