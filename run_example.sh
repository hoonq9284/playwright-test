#!/bin/bash
# ===========================================
# 스터디용 참고 스크립트 (개별 명령어 예시)
# ===========================================

# 1. 테스트만 실행
docker-compose up --build --abort-on-container-exit

# 2. Allure 리포트 생성 (Allure 3.x)
allure generate ./reports/allure-results -o ./reports/allure-report

# 3. Allure 리포트 서버 실행 (실시간 확인)
allure serve ./reports/allure-results

# 4. Allure 리포트 열기 (HTTP 서버로 제공)
allure open ./reports/allure-report

# 5. 컨테이너 정리
docker-compose down

# 6. 특정 테스트만 실행
docker-compose run test pytest tests/test_login.py -v --alluredir=/reports/allure-results

# 7. 특정 테스트 클래스만 실행
docker-compose run test pytest tests/test_login.py::TestLoginValidUsers -v --alluredir=/reports/allure-results

# 8. 키워드로 테스트 필터링
docker-compose run test pytest -k "login" -v --alluredir=/reports/allure-results
