FROM python:3.9-alpine

ARG TZ=Asia/Singapore
RUN mkdir -p /opt/web/logs /opt/web/uploads /opt/web/listener
WORKDIR /opt/web

COPY ./listener/ /opt/web/listener
COPY ./docker-entrypoint.sh /opt/web/docker-entrypoint.sh
COPY ./requirements.txt /opt/web/requirements.txt

RUN rm -rf /var/cache/apk/* /tmp/* && \
    apk update && apk upgrade && \
    apk add python3-dev libffi-dev gcc musl-dev make libmagic postgresql-dev tzdata --no-cache && \
    cp /usr/share/zoneinfo/$TZ /etc/timezone && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /opt/web/requirements.txt && \
    apk del --purge --no-cache tzdata gcc make musl-dev && \
    chmod +x /opt/web/docker-entrypoint.sh

ENTRYPOINT ["/opt/web/docker-entrypoint.sh"]