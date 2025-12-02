#!/bin/bash

# Register the cron job
# every hour execute
# docker compose run --rm watcher
echo "0 * * * * docker compose -f ${PWD}/docker-compose.yaml run --rm watcher >> ${PWD}/logs 2>&1" | crontab -