#!/bin/bash

echo Starting crontab...
cron

echo Starting supervisor...
supervisord -c /etc/supervisord.conf
