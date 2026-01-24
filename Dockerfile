FROM mcr.microsoft.com/playwright/python:v1.57.0-jammy

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all project files
COPY pages/ ./pages/
COPY tests/ ./tests/
COPY utils/ ./utils/
COPY data/ ./data/
COPY conftest.py .
COPY pytest.ini .

CMD ["pytest", "tests/", "-v", "--alluredir=/reports/allure-results"]
