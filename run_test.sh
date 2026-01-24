#!/bin/bash

docker-compose down
rm -rf ./reports/allure-results ./reports/allure-report

docker-compose up --build --abort-on-container-exit

npx allure generate ./reports/allure-results -o ./reports/allure-report --clean
npx allure open ./reports/allure-report

docker-compose down
