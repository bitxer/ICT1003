#!/bin/sh

ln -sf /usr/share/zoneinfo/$TZ /etc/timezone
ln -sf /usr/share/zoneinfo/$TZ /etc/localtime

echo "[*] Starting HTTP Listener..."
gunicorn "listener:init_app()" --bind 0.0.0.0:5000 --worker-class "gevent" --workers 3 --preload --access-logfile "/opt/web/logs/access.log" --error-logfile "/opt/web/logs/error.log"
