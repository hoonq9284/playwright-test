import pytest
import allure
from playwright.sync_api import Page

from data.users import Users, User
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@allure.feature("로그인")
@allure.story("유효한 사용자 로그인")
class TestLoginValidUsers:
    """로그인 가능한 사용자들에 대한 테스트"""

    @pytest.mark.parametrize("user", Users.get_valid_users(), ids=lambda u: u.username)
    def test_valid_user_login(self, page: Page, user: User):
        """유효한 사용자가 로그인하면 인벤토리 페이지로 이동해야 함"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        login_page.open()
        login_page.login(user.username, user.password)

        assert inventory_page.is_inventory_page(), \
            f"{user.username}: 인벤토리 페이지가 표시되어야 합니다"
        assert inventory_page.get_inventory_count() > 0, \
            f"{user.username}: 제품이 표시되어야 합니다"


@allure.feature("로그인")
@allure.story("잠긴 사용자 로그인")
class TestLoginInvalidUsers:
    """로그인 불가능한 사용자들에 대한 테스트"""

    @pytest.mark.parametrize("user", Users.get_invalid_users(), ids=lambda u: u.username)
    def test_invalid_user_login(self, page: Page, user: User):
        """잠긴 사용자가 로그인하면 에러 메시지가 표시되어야 함"""
        login_page = LoginPage(page)

        login_page.open()
        login_page.login(user.username, user.password)

        assert login_page.is_error_displayed(), \
            f"{user.username}: 에러 메시지가 표시되어야 합니다"
        assert user.expected_error in login_page.get_error_message(), \
            f"{user.username}: 예상된 에러 메시지가 표시되어야 합니다"


@allure.feature("로그인")
@allure.story("입력값 유효성 검사")
class TestLoginValidation:
    """로그인 유효성 검사 테스트"""

    def test_empty_username(self, login_page):
        """빈 사용자명으로 로그인 시 에러 메시지 표시"""
        login_page.enter_password(Users.PASSWORD)
        login_page.click_login()

        assert login_page.is_error_displayed()
        assert "Username is required" in login_page.get_error_message()

    def test_empty_password(self, login_page):
        """빈 비밀번호로 로그인 시 에러 메시지 표시"""
        login_page.enter_username(Users.STANDARD.username)
        login_page.click_login()

        assert login_page.is_error_displayed()
        assert "Password is required" in login_page.get_error_message()

    def test_empty_credentials(self, login_page):
        """빈 자격 증명으로 로그인 시 에러 메시지 표시"""
        login_page.click_login()

        assert login_page.is_error_displayed()
        assert "Username is required" in login_page.get_error_message()

    def test_invalid_username(self, login_page):
        """잘못된 사용자명으로 로그인 시 에러 메시지 표시"""
        login_page.login("invalid_user", Users.PASSWORD)

        assert login_page.is_error_displayed()
        assert "do not match" in login_page.get_error_message()

    def test_invalid_password(self, login_page):
        """잘못된 비밀번호로 로그인 시 에러 메시지 표시"""
        login_page.login(Users.STANDARD.username, "wrong_password")

        assert login_page.is_error_displayed()
        assert "do not match" in login_page.get_error_message()


@allure.feature("로그인")
@allure.story("사용자 유형별 테스트")
class TestLoginSpecificUsers:
    """각 사용자 유형별 상세 테스트"""

    def test_standard_user_can_see_all_products(self, page: Page):
        """표준 사용자가 모든 제품을 볼 수 있는지 확인"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        login_page.open()
        login_page.login(Users.STANDARD.username, Users.STANDARD.password)

        assert inventory_page.is_inventory_page()
        assert inventory_page.get_inventory_count() == 6
        assert inventory_page.get_page_title() == "Products"

    def test_locked_out_user_cannot_login(self, page: Page):
        """잠긴 사용자가 로그인할 수 없는지 확인"""
        login_page = LoginPage(page)

        login_page.open()
        login_page.login(Users.LOCKED_OUT.username, Users.LOCKED_OUT.password)

        assert login_page.is_error_displayed()
        error_msg = login_page.get_error_message()
        assert "locked out" in error_msg.lower()

    def test_problem_user_login_success(self, page: Page):
        """문제 사용자가 로그인할 수 있는지 확인"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        login_page.open()
        login_page.login(Users.PROBLEM.username, Users.PROBLEM.password)

        assert inventory_page.is_inventory_page()

    def test_performance_glitch_user_login_success(self, page: Page):
        """성능 문제 사용자가 로그인할 수 있는지 확인 (느릴 수 있음)"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        login_page.open()
        login_page.login(
            Users.PERFORMANCE_GLITCH.username,
            Users.PERFORMANCE_GLITCH.password
        )

        assert inventory_page.is_inventory_page()

    def test_error_user_login_success(self, page: Page):
        """에러 사용자가 로그인할 수 있는지 확인"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        login_page.open()
        login_page.login(Users.ERROR.username, Users.ERROR.password)

        assert inventory_page.is_inventory_page()

    def test_visual_user_login_success(self, page: Page):
        """비주얼 사용자가 로그인할 수 있는지 확인"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        login_page.open()
        login_page.login(Users.VISUAL.username, Users.VISUAL.password)

        assert inventory_page.is_inventory_page()


@allure.feature("로그인")
@allure.story("로그아웃")
class TestLogout:
    """로그아웃 테스트"""

    def test_logout_returns_to_login_page(self, logged_in_page):
        """로그아웃 후 로그인 페이지로 돌아가는지 확인"""
        logged_in_page.logout()
        login_page = LoginPage(logged_in_page.page)

        assert login_page.is_login_page()
