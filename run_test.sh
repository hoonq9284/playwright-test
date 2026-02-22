#!/bin/bash

docker-compose down
rm -rf ./reports

docker-compose up --build --abort-on-container-exit

# Allure 3 commands (npx allure ensures using Allure 3)
npx allure open reports/allure-results

docker-compose down
