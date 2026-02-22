import pytest
import allure
from playwright.sync_api import Page

from data.users import Users
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage


@allure.feature("장바구니")
@allure.story("기본 검증")
class TestCartPageBasic:
    """장바구니 페이지 기본 테스트"""

    def test_empty_cart_page(self, logged_in_page, cart_page):
        """빈 장바구니 페이지 확인"""
        logged_in_page.click_shopping_cart()

        assert cart_page.is_cart_page(), "Should be on cart page"
        assert cart_page.get_page_title() == "Your Cart"
        assert cart_page.is_cart_empty(), "Cart should be empty"
        assert cart_page.get_cart_item_count() == 0

    def test_cart_page_url_is_correct(self, logged_in_page, cart_page):
        """장바구니 페이지 URL 확인"""
        logged_in_page.click_shopping_cart()
        current_url = cart_page.get_current_url()

        assert "cart.html" in current_url, f"URL should contain 'cart.html', got '{current_url}'"


@allure.feature("장바구니")
@allure.story("상품 있는 장바구니")
class TestCartWithItems:
    """장바구니에 상품이 있는 경우 테스트"""

    def test_single_item_in_cart(self, logged_in_page, cart_page):
        """단일 상품이 장바구니에 표시되는지 확인"""
        item_names = logged_in_page.get_item_names()
        item_prices = logged_in_page.get_item_prices()
        first_item_name = item_names[0]
        first_item_price = item_prices[0]

        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.click_shopping_cart()

        assert cart_page.get_cart_item_count() == 1, "Cart should have 1 item"

        cart_names = cart_page.get_item_names()
        cart_prices = cart_page.get_item_prices()

        assert first_item_name in cart_names, f"'{first_item_name}' should be in cart"
        assert first_item_price in cart_prices, f"'{first_item_price}' should be in cart"

    def test_multiple_items_in_cart(self, logged_in_page, cart_page):
        """여러 상품이 장바구니에 표시되는지 확인"""
        item_names = logged_in_page.get_item_names()

        # 이름으로 추가 (인덱스는 버튼이 Remove로 바뀌면서 밀림)
        logged_in_page.add_item_to_cart_by_name(item_names[0])
        logged_in_page.add_item_to_cart_by_name(item_names[1])
        logged_in_page.add_item_to_cart_by_name(item_names[2])
        logged_in_page.click_shopping_cart()

        assert cart_page.get_cart_item_count() == 3, "Cart should have 3 items"

        cart_names = cart_page.get_item_names()
        assert item_names[0] in cart_names
        assert item_names[1] in cart_names
        assert item_names[2] in cart_names

    def test_all_items_in_cart(self, logged_in_page, cart_page):
        """모든 상품(6개)이 장바구니에 추가되는지 확인"""
        for i in range(6):
            logged_in_page.add_item_to_cart_by_index(0)

        logged_in_page.click_shopping_cart()

        assert cart_page.get_cart_item_count() == 6, "Cart should have 6 items"

    def test_item_quantity_is_one(self, logged_in_page, cart_page):
        """각 아이템의 수량이 1인지 확인"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.add_item_to_cart_by_index(1)
        logged_in_page.click_shopping_cart()

        quantities = cart_page.get_item_quantities()

        for qty in quantities:
            assert qty == 1, f"Each item quantity should be 1, but got {qty}"

    def test_item_description_is_displayed(self, logged_in_page, cart_page):
        """장바구니 아이템에 설명이 표시되는지 확인"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.click_shopping_cart()

        description = cart_page.get_item_description_by_index(0)

        assert len(description) > 0, "Item description should not be empty"


@allure.feature("장바구니")
@allure.story("상품 제거")
class TestCartRemoveItems:
    """장바구니 아이템 제거 테스트"""

    def test_remove_single_item_by_index(self, logged_in_page, cart_page):
        """인덱스로 단일 아이템 제거"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.add_item_to_cart_by_index(1)
        logged_in_page.click_shopping_cart()

        assert cart_page.get_cart_item_count() == 2

        cart_page.remove_item_by_index(0)

        assert cart_page.get_cart_item_count() == 1, "Cart should have 1 item after removal"

    def test_remove_all_items(self, logged_in_page, cart_page):
        """모든 아이템 제거"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.add_item_to_cart_by_index(1)
        logged_in_page.click_shopping_cart()

        # 모든 아이템 제거 (항상 첫 번째 아이템 제거)
        cart_page.remove_item_by_index(0)
        cart_page.remove_item_by_index(0)

        assert cart_page.is_cart_empty(), "Cart should be empty after removing all items"

    def test_remove_item_by_name(self, logged_in_page, cart_page):
        """이름으로 아이템 제거"""
        item_names = logged_in_page.get_item_names()
        first_item_name = item_names[0]

        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.add_item_to_cart_by_index(1)
        logged_in_page.click_shopping_cart()

        cart_page.remove_item_by_name(first_item_name)

        cart_names = cart_page.get_item_names()
        assert first_item_name not in cart_names, f"'{first_item_name}' should be removed from cart"


@allure.feature("장바구니")
@allure.story("네비게이션")
class TestCartNavigation:
    """장바구니 네비게이션 테스트"""

    def test_continue_shopping_returns_to_inventory(self, logged_in_page, cart_page):
        """'Continue Shopping' 버튼 클릭 시 인벤토리로 복귀"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.click_shopping_cart()

        cart_page.click_continue_shopping()

        assert logged_in_page.is_inventory_page(), "Should return to inventory page"

    def test_checkout_navigates_to_checkout_step_one(self, logged_in_page, cart_page, checkout_step_one_page):
        """'Checkout' 버튼 클릭 시 체크아웃 1단계로 이동"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.click_shopping_cart()

        cart_page.click_checkout()

        assert checkout_step_one_page.is_checkout_step_one_page(), "Should navigate to checkout step one"

    def test_cart_state_persists_after_continue_shopping(self, logged_in_page, cart_page):
        """'Continue Shopping' 후 장바구니 상태 유지"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.add_item_to_cart_by_index(1)
        logged_in_page.click_shopping_cart()

        assert cart_page.get_cart_item_count() == 2

        cart_page.click_continue_shopping()

        # 추가 상품 추가
        logged_in_page.add_item_to_cart_by_index(2)
        logged_in_page.click_shopping_cart()

        assert cart_page.get_cart_item_count() == 3, "Cart should have 3 items"


@allure.feature("장바구니")
@allure.story("가격 표시")
class TestCartPriceDisplay:
    """장바구니 가격 표시 테스트"""

    def test_prices_match_inventory_prices(self, logged_in_page, cart_page):
        """장바구니 가격이 인벤토리 가격과 일치하는지 확인"""
        item_names = logged_in_page.get_item_names()
        inventory_prices = logged_in_page.get_item_prices()

        # 이름으로 추가하여 정확한 상품 선택
        logged_in_page.add_item_to_cart_by_name(item_names[0])
        logged_in_page.add_item_to_cart_by_name(item_names[1])
        logged_in_page.click_shopping_cart()

        cart_prices = cart_page.get_item_prices()

        assert inventory_prices[0] in cart_prices
        assert inventory_prices[1] in cart_prices

    def test_all_prices_have_dollar_sign(self, logged_in_page, cart_page):
        """모든 가격에 $ 기호가 있는지 확인"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.add_item_to_cart_by_index(1)
        logged_in_page.click_shopping_cart()

        cart_prices = cart_page.get_item_prices()

        for price in cart_prices:
            assert price.startswith("$"), f"Price should start with $, got '{price}'"


@allure.feature("장바구니")
@allure.story("빈 장바구니 체크아웃")
class TestCartEmptyCheckout:
    """빈 장바구니 체크아웃 테스트"""

    def test_checkout_with_empty_cart(self, logged_in_page, cart_page, checkout_step_one_page):
        """빈 장바구니로 체크아웃 시도"""
        logged_in_page.click_shopping_cart()

        assert cart_page.is_cart_empty()

        # 빈 장바구니에서도 체크아웃 버튼은 클릭 가능
        cart_page.click_checkout()

        # 체크아웃 페이지로 이동은 되지만, 실제 주문은 불가능할 수 있음
        assert checkout_step_one_page.is_checkout_step_one_page()


@allure.feature("장바구니")
@allure.story("아이템 클릭")
class TestCartItemClickable:
    """장바구니 아이템 클릭 테스트"""

    def test_click_item_name_navigates_to_detail(self, logged_in_page, cart_page):
        """장바구니에서 아이템 이름 클릭 시 상세 페이지로 이동"""
        item_names = logged_in_page.get_item_names()
        first_item_name = item_names[0]

        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.click_shopping_cart()

        # 아이템 이름 클릭
        cart_page.page.locator(".inventory_item_name", has_text=first_item_name).click()

        # URL이 inventory-item.html을 포함하는지 확인
        current_url = cart_page.get_current_url()
        assert "inventory-item.html" in current_url, "Should navigate to product detail page"
