from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.config import Config


class CartPage(BasePage):
    """장바구니 페이지 객체"""

    # Selectors
    CART_LIST = ".cart_list"
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    CART_ITEM_QUANTITY = ".cart_quantity"
    CART_ITEM_DESC = ".inventory_item_desc"
    REMOVE_BUTTON = "button[data-test^='remove']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    PAGE_TITLE = ".title"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{Config.BASE_URL}/cart.html"

    def open(self):
        """장바구니 페이지 열기"""
        self.navigate(self.url)
        return self

    def is_cart_page(self) -> bool:
        """현재 페이지가 장바구니 페이지인지 확인"""
        return self.is_visible(self.CART_LIST, timeout=5000)

    def get_page_title(self) -> str:
        """페이지 타이틀 반환"""
        return self.get_text(self.PAGE_TITLE)

    def get_cart_item_count(self) -> int:
        """장바구니 아이템 개수 반환"""
        return self.get_element_count(self.CART_ITEM)

    def get_item_names(self) -> list[str]:
        """장바구니 내 모든 아이템 이름 반환"""
        elements = self.page.locator(self.CART_ITEM_NAME).all()
        return [el.text_content() or "" for el in elements]

    def get_item_prices(self) -> list[str]:
        """장바구니 내 모든 아이템 가격 반환"""
        elements = self.page.locator(self.CART_ITEM_PRICE).all()
        return [el.text_content() or "" for el in elements]

    def get_item_quantities(self) -> list[int]:
        """장바구니 내 모든 아이템 수량 반환"""
        elements = self.page.locator(self.CART_ITEM_QUANTITY).all()
        return [int(el.text_content() or "0") for el in elements]

    def remove_item_by_index(self, index: int = 0):
        """인덱스로 아이템 제거"""
        buttons = self.page.locator(self.REMOVE_BUTTON).all()
        if index < len(buttons):
            buttons[index].click()
        return self

    def remove_item_by_name(self, item_name: str):
        """이름으로 아이템 제거"""
        # 아이템 이름을 기반으로 remove 버튼 찾기
        item_id = item_name.lower().replace(" ", "-")
        remove_selector = f"[data-test='remove-{item_id}']"
        if self.is_visible(remove_selector, timeout=2000):
            self.click(remove_selector)
        return self

    def click_continue_shopping(self):
        """쇼핑 계속하기 버튼 클릭"""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        return self

    def click_checkout(self):
        """체크아웃 버튼 클릭"""
        self.click(self.CHECKOUT_BUTTON)
        return self

    def is_cart_empty(self) -> bool:
        """장바구니가 비어있는지 확인"""
        return self.get_cart_item_count() == 0

    def get_item_description_by_index(self, index: int = 0) -> str:
        """인덱스로 아이템 설명 반환"""
        elements = self.page.locator(self.CART_ITEM_DESC).all()
        if index < len(elements):
            return elements[index].text_content() or ""
        return ""
