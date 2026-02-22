#!/bin/bash

docker-compose down
rm -rf ./reports

docker-compose up --build --abort-on-container-exit

allure generate ./reports/allure-results -o ./reports/allure-report
allure open ./reports/allure-report

docker-compose down
