import pytest
from playwright.sync_api import Page

from data.users import Users
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage


class TestProductDetailNavigation:
    """상품 상세 페이지 네비게이션 테스트"""

    def test_click_product_name_navigates_to_detail(self, logged_in_page, product_detail_page):
        """상품 이름 클릭 시 상세 페이지로 이동"""
        product_names = logged_in_page.get_item_names()
        first_product_name = product_names[0]

        logged_in_page.click_product_by_index(0)

        assert product_detail_page.is_product_detail_page(), "Should navigate to product detail page"
        assert product_detail_page.get_product_name() == first_product_name

    def test_click_product_image_navigates_to_detail(self, logged_in_page, product_detail_page):
        """상품 이미지 클릭 시 상세 페이지로 이동"""
        product_names = logged_in_page.get_item_names()
        first_product_name = product_names[0]

        logged_in_page.click_product_image_by_index(0)

        assert product_detail_page.is_product_detail_page(), "Should navigate to product detail page"
        assert product_detail_page.get_product_name() == first_product_name

    def test_back_to_products_returns_to_inventory(self, logged_in_page, product_detail_page):
        """'Back to products' 버튼 클릭 시 인벤토리 페이지로 복귀"""
        logged_in_page.click_product_by_index(0)

        assert product_detail_page.is_product_detail_page()

        product_detail_page.click_back_to_products()

        assert logged_in_page.is_inventory_page(), "Should return to inventory page"


class TestProductDetailContent:
    """상품 상세 페이지 컨텐츠 테스트"""

    @pytest.fixture
    def product_detail_with_info(self, logged_in_page, product_detail_page):
        """상품 상세 페이지로 이동 (상품 정보 포함)"""
        # 인벤토리에서 첫 번째 상품 정보 저장
        names = logged_in_page.get_item_names()
        prices = logged_in_page.get_item_prices()

        info = {
            "name": names[0],
            "price": prices[0]
        }

        logged_in_page.click_product_by_index(0)
        return product_detail_page, info

    def test_product_name_is_displayed(self, product_detail_with_info):
        """상품 이름이 표시되는지 확인"""
        detail_page, info = product_detail_with_info
        product_name = detail_page.get_product_name()

        assert product_name == info["name"], f"Expected '{info['name']}', but got '{product_name}'"
        assert len(product_name) > 0, "Product name should not be empty"

    def test_product_price_is_displayed(self, product_detail_with_info):
        """상품 가격이 표시되는지 확인"""
        detail_page, info = product_detail_with_info
        product_price = detail_page.get_product_price()

        assert product_price == info["price"], f"Expected '{info['price']}', but got '{product_price}'"
        assert product_price.startswith("$"), "Price should start with $"

    def test_product_description_is_displayed(self, product_detail_with_info):
        """상품 설명이 표시되는지 확인"""
        detail_page, _ = product_detail_with_info
        description = detail_page.get_product_description()

        assert len(description) > 0, "Product description should not be empty"

    def test_product_image_is_displayed(self, product_detail_with_info):
        """상품 이미지가 표시되는지 확인"""
        detail_page, _ = product_detail_with_info

        assert detail_page.is_product_image_displayed(), "Product image should be displayed"

    def test_product_image_has_valid_src(self, product_detail_with_info):
        """상품 이미지 src가 유효한지 확인"""
        detail_page, _ = product_detail_with_info
        image_src = detail_page.get_product_image_src()

        assert len(image_src) > 0, "Image src should not be empty"
        assert "static/media" in image_src or "jpg" in image_src or "png" in image_src


class TestProductDetailCartOperations:
    """상품 상세 페이지에서 장바구니 조작 테스트"""

    def test_add_to_cart_button_visible_initially(self, logged_in_page, product_detail_page):
        """초기 상태에서 'Add to cart' 버튼이 표시되는지 확인"""
        logged_in_page.click_product_by_index(0)

        assert product_detail_page.is_add_to_cart_visible(), "'Add to cart' button should be visible"
        assert not product_detail_page.is_remove_visible(), "'Remove' button should not be visible"

    def test_add_to_cart_from_detail_page(self, logged_in_page, product_detail_page):
        """상품 상세 페이지에서 장바구니 추가"""
        logged_in_page.click_product_by_index(0)
        product_detail_page.add_to_cart()
        badge_count = product_detail_page.get_cart_badge_count()

        assert badge_count == 1, f"Cart badge should show 1, but got {badge_count}"

    def test_button_changes_to_remove_after_add(self, logged_in_page, product_detail_page):
        """장바구니 추가 후 버튼이 'Remove'로 변경되는지 확인"""
        logged_in_page.click_product_by_index(0)
        product_detail_page.add_to_cart()

        assert product_detail_page.is_remove_visible(), "'Remove' button should be visible after add"
        assert not product_detail_page.is_add_to_cart_visible(), "'Add to cart' should not be visible"

    def test_remove_from_cart_on_detail_page(self, logged_in_page, product_detail_page):
        """상품 상세 페이지에서 장바구니 제거"""
        logged_in_page.click_product_by_index(0)
        product_detail_page.add_to_cart()

        assert product_detail_page.get_cart_badge_count() == 1

        product_detail_page.remove_from_cart()
        badge_count = product_detail_page.get_cart_badge_count()

        assert badge_count == 0, "Cart should be empty after removal"
        assert product_detail_page.is_add_to_cart_visible(), "'Add to cart' should be visible again"

    def test_navigate_to_cart_from_detail_page(self, logged_in_page, product_detail_page, cart_page):
        """상품 상세 페이지에서 장바구니로 이동"""
        logged_in_page.click_product_by_index(0)
        product_detail_page.add_to_cart()
        product_detail_page.click_shopping_cart()

        assert cart_page.is_cart_page(), "Should navigate to cart page"
        assert cart_page.get_cart_item_count() == 1


class TestAllProductsDetail:
    """모든 상품 상세 페이지 테스트"""

    EXPECTED_PRODUCTS = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)"
    ]

    @pytest.mark.parametrize("product_index", range(6))
    def test_each_product_has_valid_detail_page(self, logged_in_page, product_detail_page, product_index):
        """각 상품이 유효한 상세 페이지를 가지는지 확인"""
        logged_in_page.click_product_by_index(product_index)

        assert product_detail_page.is_product_detail_page(), f"Product {product_index} should have detail page"
        assert len(product_detail_page.get_product_name()) > 0
        assert len(product_detail_page.get_product_description()) > 0
        assert product_detail_page.get_product_price().startswith("$")
        assert product_detail_page.is_product_image_displayed()


class TestProductDetailPersistence:
    """상품 상세 페이지 상태 유지 테스트"""

    def test_cart_state_persists_when_returning_to_inventory(self, logged_in_page, product_detail_page):
        """상세 페이지에서 장바구니 추가 후 인벤토리로 돌아가도 상태 유지"""
        logged_in_page.click_product_by_index(0)
        product_detail_page.add_to_cart()
        product_detail_page.click_back_to_products()

        badge_count = logged_in_page.get_cart_badge_count()
        assert badge_count == 1, "Cart state should persist"

        # Remove 버튼이 표시되어야 함
        remove_count = logged_in_page.get_remove_button_count()
        assert remove_count == 1, "Remove button should be visible for added item"

    def test_add_multiple_from_different_detail_pages(self, logged_in_page, product_detail_page):
        """여러 상품 상세 페이지에서 장바구니 추가"""
        # 첫 번째 상품 추가
        logged_in_page.click_product_by_index(0)
        product_detail_page.add_to_cart()
        product_detail_page.click_back_to_products()

        # 두 번째 상품 추가
        logged_in_page.click_product_by_index(1)
        product_detail_page.add_to_cart()
        product_detail_page.click_back_to_products()

        # 세 번째 상품 추가
        logged_in_page.click_product_by_index(2)
        product_detail_page.add_to_cart()

        badge_count = product_detail_page.get_cart_badge_count()
        assert badge_count == 3, f"Cart should have 3 items, but got {badge_count}"
