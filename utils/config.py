import os


class Config:
    """테스트 설정"""

    # 타임아웃 설정
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10")) * 1000  # ms
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30")) * 1000  # ms

    # 리포트 설정
    REPORTS_DIR = os.getenv("REPORTS_DIR", "/reports")
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"

    # 테스트 대상 URL
    BASE_URL = "https://www.saucedemo.com"

    # 브라우저 설정
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
