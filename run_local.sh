#!/bin/bash
# 로컬에서 브라우저를 보면서 테스트 실행

set -e

# 결과 폴더 정리
rm -rf ./reports/allure-results ./reports/allure-report
mkdir -p ./reports/allure-results

# 브라우저 모드 선택
MODE=${1:-headed}  # headed 또는 headless (기본값: headed)

if [ "$MODE" = "headed" ]; then
    echo "Running tests with visible browser..."
    HEADLESS=false pytest tests/ -v --headed --alluredir=./reports/allure-results
else
    echo "Running tests in headless mode..."
    HEADLESS=true pytest tests/ -v --alluredir=./reports/allure-results
fi

# Allure 리포트 생성 및 열기
npx allure generate ./reports/allure-results -o ./reports/allure-report --clean
npx allure open ./reports/allure-report
