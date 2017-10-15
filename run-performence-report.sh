#!/bin/bash
docker-compose -f docker-compose.performence.yml run k6 run --vus $1 --duration 10s /script/report.js
