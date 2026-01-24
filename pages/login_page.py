from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.config import Config

class LoginPage(BasePage):
    """로그인 페이지 객체 (Playwright)"""

    # Selectors
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_BUTTON = ".error-button"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = Config.BASE_URL

    def open(self):
        """로그인 페이지 열기"""
        self.navigate(self.url)
        return self

    def enter_username(self, username: str):
        """사용자명 입력"""
        self.fill(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        """비밀번호 입력"""
        self.fill(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """로그인 버튼 클릭"""
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str):
        """로그인 수행"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self) -> str:
        """에러 메시지 텍스트 반환"""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """에러 메시지가 표시되는지 확인"""
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)

    def close_error(self):
        """에러 메시지 닫기"""
        self.click(self.ERROR_BUTTON)
        return self

    def is_login_page(self) -> bool:
        """현재 페이지가 로그인 페이지인지 확인"""
        return self.is_visible(self.LOGIN_BUTTON, timeout=3000)
