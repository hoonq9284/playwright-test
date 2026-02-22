import pytest
from playwright.sync_api import Page

from data.users import Users
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestInventoryPage:
    """인벤토리 페이지 기본 테스트"""

    def test_inventory_displays_six_products(self, logged_in_page):
        """인벤토리에 6개의 제품이 표시되는지 확인"""
        count = logged_in_page.get_inventory_count()

        assert count == 6, f"Expected 6 products, but found {count}"

    def test_inventory_page_title(self, logged_in_page):
        """인벤토리 페이지 제목이 'Products'인지 확인"""
        title = logged_in_page.get_page_title()

        assert title == "Products", f"Expected 'Products', but got '{title}'"

    def test_all_products_have_names(self, logged_in_page):
        """모든 제품에 이름이 있는지 확인"""
        names = logged_in_page.get_item_names()

        assert len(names) == 6, f"Expected 6 product names, but found {len(names)}"
        for name in names:
            assert len(name) > 0, "Product name should not be empty"

    def test_all_products_have_prices(self, logged_in_page):
        """모든 제품에 가격이 있고 $ 기호로 시작하는지 확인"""
        prices = logged_in_page.get_item_prices()

        assert len(prices) == 6, f"Expected 6 prices, but found {len(prices)}"
        for price in prices:
            assert price.startswith("$"), f"Price should start with $, but got '{price}'"

    def test_all_products_have_descriptions(self, logged_in_page):
        """모든 제품에 설명이 있는지 확인"""
        descriptions = logged_in_page.get_item_descriptions()

        assert len(descriptions) == 6, f"Expected 6 descriptions, but found {len(descriptions)}"
        for desc in descriptions:
            assert len(desc) > 0, "Product description should not be empty"

    def test_all_products_have_add_to_cart_button(self, logged_in_page):
        """모든 제품에 'Add to cart' 버튼이 있는지 확인"""
        button_count = logged_in_page.get_add_to_cart_button_count()

        assert button_count == 6, f"Expected 6 'Add to cart' buttons, but found {button_count}"

    def test_inventory_url_is_correct(self, logged_in_page):
        """인벤토리 페이지 URL이 올바른지 확인"""
        current_url = logged_in_page.get_current_url()

        assert "inventory.html" in current_url, f"URL should contain 'inventory.html', but got '{current_url}'"


class TestProductSorting:
    """제품 정렬 테스트"""

    def test_default_sort_is_az(self, logged_in_page):
        """기본 정렬이 A-Z인지 확인"""
        sort_option = logged_in_page.get_current_sort_option()

        assert sort_option == "az", f"Default sort should be 'az', but got '{sort_option}'"

    def test_sort_by_name_ascending(self, logged_in_page):
        """이름 오름차순 정렬 (A to Z)"""
        logged_in_page.sort_by_name_asc()
        names = logged_in_page.get_item_names()
        sorted_names = sorted(names)

        assert names == sorted_names, "Products should be sorted A-Z"

    def test_sort_by_name_descending(self, logged_in_page):
        """이름 내림차순 정렬 (Z to A)"""
        logged_in_page.sort_by_name_desc()
        names = logged_in_page.get_item_names()
        sorted_names = sorted(names, reverse=True)

        assert names == sorted_names, "Products should be sorted Z-A"

    def test_sort_by_price_low_to_high(self, logged_in_page):
        """가격 오름차순 정렬 (Low to High)"""
        logged_in_page.sort_by_price_asc()
        prices = logged_in_page.get_item_prices_as_float()

        assert prices == sorted(prices), "Products should be sorted by price low to high"

    def test_sort_by_price_high_to_low(self, logged_in_page):
        """가격 내림차순 정렬 (High to Low)"""
        logged_in_page.sort_by_price_desc()
        prices = logged_in_page.get_item_prices_as_float()

        assert prices == sorted(prices, reverse=True), "Products should be sorted by price high to low"

    def test_sort_option_persists(self, logged_in_page):
        """정렬 옵션이 유지되는지 확인"""
        logged_in_page.sort_by_price_desc()
        current_option = logged_in_page.get_current_sort_option()

        assert current_option == "hilo", "Sort option should persist after selection"


class TestShoppingCartFromInventory:
    """인벤토리에서 장바구니 추가/제거 테스트"""

    def test_add_single_item_to_cart(self, logged_in_page):
        """단일 제품을 장바구니에 추가"""
        logged_in_page.add_item_to_cart_by_index(0)
        badge_count = logged_in_page.get_cart_badge_count()

        assert badge_count == 1, f"Cart badge should show 1, but got {badge_count}"

    def test_add_multiple_items_to_cart(self, logged_in_page):
        """여러 제품을 장바구니에 추가"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.add_item_to_cart_by_index(1)
        logged_in_page.add_item_to_cart_by_index(2)
        badge_count = logged_in_page.get_cart_badge_count()

        assert badge_count == 3, f"Cart badge should show 3, but got {badge_count}"

    def test_add_all_items_to_cart(self, logged_in_page):
        """모든 제품을 장바구니에 추가"""
        for i in range(6):
            logged_in_page.add_item_to_cart_by_index(0)  # 추가 후 버튼이 Remove로 바뀌므로 항상 0번째
        badge_count = logged_in_page.get_cart_badge_count()

        assert badge_count == 6, f"Cart badge should show 6, but got {badge_count}"

    def test_button_changes_to_remove_after_add(self, logged_in_page):
        """장바구니 추가 후 버튼이 'Remove'로 변경되는지 확인"""
        initial_add_count = logged_in_page.get_add_to_cart_button_count()
        logged_in_page.add_item_to_cart_by_index(0)
        new_add_count = logged_in_page.get_add_to_cart_button_count()
        remove_count = logged_in_page.get_remove_button_count()

        assert new_add_count == initial_add_count - 1, "Add to cart button count should decrease by 1"
        assert remove_count == 1, "Remove button should appear"

    def test_remove_item_from_cart_on_inventory_page(self, logged_in_page):
        """인벤토리 페이지에서 장바구니 제거"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.add_item_to_cart_by_index(1)

        assert logged_in_page.get_cart_badge_count() == 2

        logged_in_page.remove_item_from_cart_by_index(0)
        badge_count = logged_in_page.get_cart_badge_count()

        assert badge_count == 1, f"Cart badge should show 1 after removal, but got {badge_count}"

    def test_navigate_to_cart_page(self, logged_in_page, cart_page):
        """장바구니 아이콘 클릭 시 장바구니 페이지로 이동"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.click_shopping_cart()

        assert cart_page.is_cart_page(), "Should navigate to cart page"
        assert cart_page.get_page_title() == "Your Cart", f"Cart page title should be 'Your Cart'"


class TestMenuNavigation:
    """메뉴 네비게이션 테스트"""

    def test_open_and_close_menu(self, logged_in_page):
        """햄버거 메뉴 열기/닫기"""
        logged_in_page.open_menu()

        assert logged_in_page.is_visible("#logout_sidebar_link"), "Menu should be open"

        logged_in_page.close_menu()
        # 메뉴 닫힌 후 약간의 대기
        logged_in_page.page.wait_for_timeout(500)

    def test_all_items_menu_navigates_to_inventory(self, logged_in_page):
        """'All Items' 메뉴 클릭 시 인벤토리 페이지로 이동"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.click_shopping_cart()
        # 장바구니 페이지에서 'All Items' 클릭
        logged_in_page.click_all_items()

        assert logged_in_page.is_inventory_page(), "Should navigate to inventory page"

    def test_reset_app_state_clears_cart(self, logged_in_page):
        """'Reset App State'가 장바구니를 초기화하는지 확인"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.add_item_to_cart_by_index(1)

        assert logged_in_page.get_cart_badge_count() == 2

        logged_in_page.reset_app_state()
        logged_in_page.close_menu()
        logged_in_page.page.wait_for_timeout(500)
        badge_count = logged_in_page.get_cart_badge_count()

        assert badge_count == 0, "Cart should be empty after reset"

    def test_logout_from_inventory_page(self, logged_in_page):
        """인벤토리 페이지에서 로그아웃"""
        logged_in_page.logout()
        login_page = LoginPage(logged_in_page.page)

        assert login_page.is_login_page(), "Should return to login page after logout"
        assert "saucedemo.com" in logged_in_page.get_current_url()


class TestFooter:
    """푸터 테스트"""

    def test_footer_is_visible(self, logged_in_page):
        """푸터가 표시되는지 확인"""
        assert logged_in_page.is_footer_visible(), "Footer should be visible"

    def test_twitter_link_exists(self, logged_in_page):
        """Twitter 링크가 존재하는지 확인"""
        twitter_link = logged_in_page.get_twitter_link()

        assert "twitter.com" in twitter_link.lower(), f"Twitter link should exist, got '{twitter_link}'"

    def test_facebook_link_exists(self, logged_in_page):
        """Facebook 링크가 존재하는지 확인"""
        facebook_link = logged_in_page.get_facebook_link()

        assert "facebook.com" in facebook_link.lower(), f"Facebook link should exist, got '{facebook_link}'"

    def test_linkedin_link_exists(self, logged_in_page):
        """LinkedIn 링크가 존재하는지 확인"""
        linkedin_link = logged_in_page.get_linkedin_link()

        assert "linkedin.com" in linkedin_link.lower(), f"LinkedIn link should exist, got '{linkedin_link}'"


class TestProblemUser:
    """문제 사용자에 대한 테스트"""

    @pytest.fixture
    def problem_user_page(self, page: Page):
        """문제 사용자로 로그인된 상태"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(Users.PROBLEM.username, Users.PROBLEM.password)
        return InventoryPage(page)

    def test_problem_user_sees_products(self, problem_user_page):
        """문제 사용자가 제품을 볼 수 있는지 확인"""
        assert problem_user_page.is_inventory_page()
        assert problem_user_page.get_inventory_count() == 6

    def test_problem_user_can_add_to_cart(self, problem_user_page):
        """문제 사용자가 장바구니에 추가할 수 있는지 확인"""
        problem_user_page.add_item_to_cart_by_index(0)
        badge_count = problem_user_page.get_cart_badge_count()

        assert badge_count == 1, f"Cart badge should show 1, but got {badge_count}"


class TestErrorUser:
    """에러 사용자에 대한 테스트"""

    @pytest.fixture
    def error_user_page(self, page: Page):
        """에러 사용자로 로그인된 상태"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(Users.ERROR.username, Users.ERROR.password)
        return InventoryPage(page)

    def test_error_user_sees_products(self, error_user_page):
        """에러 사용자가 제품을 볼 수 있는지 확인"""
        assert error_user_page.is_inventory_page()
        assert error_user_page.get_inventory_count() == 6
