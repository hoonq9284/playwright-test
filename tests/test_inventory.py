import pytest
from playwright.sync_api import Page

from data.users import Users
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestInventoryPage:
    """인벤토리 페이지 테스트"""

    def test_inventory_displays_six_products(self, logged_in_page):
        """인벤토리에 6개의 제품이 표시되는지 확인"""
        assert logged_in_page.get_inventory_count() == 6

    def test_inventory_page_title(self, logged_in_page):
        """인벤토리 페이지 제목 확인"""
        assert logged_in_page.get_page_title() == "Products"

    def test_all_products_have_names(self, logged_in_page):
        """모든 제품에 이름이 있는지 확인"""
        names = logged_in_page.get_item_names()
        assert len(names) == 6
        for name in names:
            assert len(name) > 0

    def test_all_products_have_prices(self, logged_in_page):
        """모든 제품에 가격이 있는지 확인"""
        prices = logged_in_page.get_item_prices()
        assert len(prices) == 6
        for price in prices:
            assert price.startswith("$")


class TestShoppingCart:
    """장바구니 테스트"""

    def test_add_item_to_cart(self, logged_in_page):
        """제품을 장바구니에 추가할 수 있는지 확인"""
        logged_in_page.add_item_to_cart_by_index(0)
        assert logged_in_page.get_cart_badge_count() == 1

    def test_add_multiple_items_to_cart(self, logged_in_page):
        """여러 제품을 장바구니에 추가할 수 있는지 확인"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.add_item_to_cart_by_index(1)
        logged_in_page.add_item_to_cart_by_index(2)
        assert logged_in_page.get_cart_badge_count() == 3


class TestProblemUser:
    """문제 사용자에 대한 특별 테스트"""

    @pytest.fixture
    def problem_user_logged_in(self, page: Page):
        """문제 사용자로 로그인"""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        login_page.open()
        login_page.login(Users.PROBLEM.username, Users.PROBLEM.password)

        return inventory_page

    def test_problem_user_sees_products(self, problem_user_logged_in):
        """문제 사용자가 제품을 볼 수 있는지 확인"""
        assert problem_user_logged_in.is_inventory_page()
        assert problem_user_logged_in.get_inventory_count() == 6
