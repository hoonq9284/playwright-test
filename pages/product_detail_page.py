from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.config import Config


class ProductDetailPage(BasePage):
    """상품 상세 페이지 객체"""

    # Selectors
    INVENTORY_DETAILS = ".inventory_details"
    PRODUCT_NAME = ".inventory_details_name"
    PRODUCT_DESC = ".inventory_details_desc"
    PRODUCT_PRICE = ".inventory_details_price"
    PRODUCT_IMAGE = ".inventory_details_img"
    ADD_TO_CART_BUTTON = "[data-test^='add-to-cart']"
    REMOVE_BUTTON = "[data-test^='remove']"
    BACK_BUTTON = "[data-test='back-to-products']"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    SHOPPING_CART_LINK = ".shopping_cart_link"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{Config.BASE_URL}/inventory-item.html"

    def is_product_detail_page(self) -> bool:
        """현재 페이지가 상품 상세 페이지인지 확인"""
        return self.is_visible(self.INVENTORY_DETAILS, timeout=5000)

    def get_product_name(self) -> str:
        """상품 이름 반환"""
        return self.get_text(self.PRODUCT_NAME)

    def get_product_description(self) -> str:
        """상품 설명 반환"""
        return self.get_text(self.PRODUCT_DESC)

    def get_product_price(self) -> str:
        """상품 가격 반환"""
        return self.get_text(self.PRODUCT_PRICE)

    def get_product_price_value(self) -> float:
        """상품 가격 숫자 값 반환"""
        price = self.get_product_price()
        return float(price.replace("$", "")) if price else 0.0

    def is_product_image_displayed(self) -> bool:
        """상품 이미지가 표시되는지 확인"""
        return self.is_visible(self.PRODUCT_IMAGE, timeout=3000)

    def get_product_image_src(self) -> str:
        """상품 이미지 src 반환"""
        img = self.page.locator(self.PRODUCT_IMAGE)
        return img.get_attribute("src") or ""

    def add_to_cart(self):
        """장바구니에 추가"""
        self.click(self.ADD_TO_CART_BUTTON)
        return self

    def remove_from_cart(self):
        """장바구니에서 제거"""
        self.click(self.REMOVE_BUTTON)
        return self

    def is_add_to_cart_visible(self) -> bool:
        """장바구니 추가 버튼이 표시되는지 확인"""
        return self.is_visible(self.ADD_TO_CART_BUTTON, timeout=2000)

    def is_remove_visible(self) -> bool:
        """제거 버튼이 표시되는지 확인"""
        return self.is_visible(self.REMOVE_BUTTON, timeout=2000)

    def click_back_to_products(self):
        """제품 목록으로 돌아가기"""
        self.click(self.BACK_BUTTON)
        return self

    def get_cart_badge_count(self) -> int:
        """장바구니 배지 숫자 반환"""
        if self.is_visible(self.SHOPPING_CART_BADGE, timeout=2000):
            text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(text) if text else 0
        return 0

    def click_shopping_cart(self):
        """장바구니 클릭"""
        self.click(self.SHOPPING_CART_LINK)
        return self
