# playwright 공식 이미지 설치
FROM mcr.microsoft.com/playwright/python:v1.57.0-jammy

# 작업 디렉토리 /app 으로 세팅 (이후 모든 명령어는 /app 위치에서 실행됨)
WORKDIR /app
ENV PYTHONPATH=/app

# 로컬 환경의 requirements.txt를 컨테이너로 복사
COPY requirements.txt .
# 이미지 빌드할 때 필요 라이브러리 설치
RUN pip install -r requirements.txt

# 전체 프로젝트 파일 컨테이너에 복사
COPY pages/ ./pages/
COPY tests/ ./tests/
COPY utils/ ./utils/
COPY data/ ./data/
COPY conftest.py .
COPY pytest.ini .

# 컨테이너가 시작될 때 명령어 실행
CMD ["pytest", "tests/", "-v", "--alluredir=/reports/allure-results"]
