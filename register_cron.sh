#!/bin/bash

# Register the cron job
# every hour execute
# docker compose run --rm watcher

sudo systemctl enable cron
sudo systemctl start cron

echo "0 * * * * docker compose -f ${PWD}/docker-compose.yaml run --rm stock_watcher >> ${PWD}/logs 2>&1" | crontab -