#!/bin/bash
set -e

cleanup() {
    echo "컨테이너 정리 중..."
    docker-compose down
}
trap cleanup EXIT INT TERM

docker-compose down
rm -rf ./reports

docker-compose up --build --abort-on-container-exit

allure generate ./reports/allure-results -o ./reports/allure-report
allure open ./reports/allure-report
