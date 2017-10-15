#!/bin/bash

docker-compose up --scale db_saver=$1 --scale car_simulator=$2 --scale report_worker=$3 -d
