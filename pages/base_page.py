from playwright.sync_api import Page, expect
from utils.config import Config


class BasePage:
    """모든 페이지 객체의 기본 클래스 (Playwright)"""

    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(Config.DEFAULT_TIMEOUT)

    def navigate(self, url: str):
        """URL로 이동"""
        self.page.goto(url)
        return self

    def click(self, selector: str):
        """요소 클릭"""
        self.page.click(selector)
        return self

    def fill(self, selector: str, text: str):
        """텍스트 입력"""
        self.page.fill(selector, text)
        return self

    def get_text(self, selector: str) -> str:
        """요소의 텍스트 반환"""
        return self.page.text_content(selector) or ""

    def is_visible(self, selector: str, timeout: int = None) -> bool:
        """요소가 보이는지 확인"""
        try:
            self.page.wait_for_selector(
                selector,
                state="visible",
                timeout=timeout or Config.DEFAULT_TIMEOUT
            )
            return True
        except:
            return False

    def wait_for_selector(self, selector: str, state: str = "visible"):
        """요소 대기"""
        self.page.wait_for_selector(selector, state=state)
        return self

    def get_elements(self, selector: str):
        """여러 요소 반환"""
        return self.page.locator(selector).all()

    def get_element_count(self, selector: str) -> int:
        """요소 개수 반환"""
        return self.page.locator(selector).count()

    def get_current_url(self) -> str:
        """현재 URL 반환"""
        return self.page.url

    def get_title(self) -> str:
        """페이지 타이틀 반환"""
        return self.page.title()

    def take_screenshot(self, path: str):
        """스크린샷 저장"""
        self.page.screenshot(path=path)

    def get_screenshot_bytes(self) -> bytes:
        """스크린샷 바이트 반환"""
        return self.page.screenshot()
