# 1. Make configuration file for Celery service

`nano /etc/conf.d/celery-sound_annotation
`

```
# Name of nodes to start
# here we have a single node
CELERYD_NODES="w1"
# or we could have three nodes:
#CELERYD_NODES="w1 w2 w3"

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/home/audio_annotation/venv/bin/celery"
#CELERY_BIN="/home/audio_annotation/venv/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="audioan"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# How to call manage.py
CELERYD_MULTI="multi"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"

# - %n will be replaced with the first part of the nodename.
# - %I will be replaced with the current child process index
#   and is important when using the prefork pool to avoid race conditions.
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="INFO"
```

# 2. Make Celery Service

```

[Unit]
Description=Celery Service for sound_annotation
After=network.target

[Service]
Type=forking
User=root
Group=root
EnvironmentFile=/etc/conf.d/celery-sound_annotation
WorkingDirectory=/home/audio_annotation/
ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}"'
ExecReload=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi restart $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
Restart=always

[Install]
WantedBy=multi-user.target

```

# 3. Install Redis and persist on boot

```
sudo apt install redis-server
sudo nano /etc/redis/redis.conf
```

#### 3.1 Next, find the line specifying the supervised directive. By default, this line is set to no. However, to manage Redis as a service, set the supervised directive to systemd (Ubuntu’s init system).

```
sudo apt start redis-server
sudo apt enable redis-server
```

# 4. Start Celery Service and make it start on boot

```
systemctl start celery-sound_annotation.service
systemctl enable celery-sound_annotation.service
systemctl status celery-sound_annotation.service
```

# 5. Check logs

```
watch tail  /var/log/celery/w1.log
```
