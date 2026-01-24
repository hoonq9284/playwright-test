from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.config import Config


class InventoryPage(BasePage):
    """인벤토리(제품 목록) 페이지 객체 (Playwright)"""

    # Selectors
    INVENTORY_LIST = ".inventory_list"
    INVENTORY_ITEM = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    INVENTORY_ITEM_DESC = ".inventory_item_desc"
    ADD_TO_CART_BUTTON = "button[data-test^='add-to-cart']"
    REMOVE_BUTTON = "button[data-test^='remove']"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    SORT_DROPDOWN = ".product_sort_container"
    PAGE_TITLE = ".title"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = Config.BASE_URL

    def is_inventory_page(self) -> bool:
        """현재 페이지가 인벤토리 페이지인지 확인"""
        return self.is_visible(self.INVENTORY_LIST, timeout=5000)

    def get_page_title(self) -> str:
        """페이지 타이틀 반환"""
        return self.get_text(self.PAGE_TITLE)

    def get_inventory_count(self) -> int:
        """인벤토리 아이템 개수 반환"""
        return self.get_element_count(self.INVENTORY_ITEM)

    def get_item_names(self) -> list[str]:
        """모든 아이템 이름 목록 반환"""
        elements = self.page.locator(self.INVENTORY_ITEM_NAME).all()
        return [el.text_content() or "" for el in elements]

    def get_item_prices(self) -> list[str]:
        """모든 아이템 가격 목록 반환"""
        elements = self.page.locator(self.INVENTORY_ITEM_PRICE).all()
        return [el.text_content() or "" for el in elements]

    def add_item_to_cart_by_index(self, index: int = 0):
        """인덱스로 아이템을 장바구니에 추가"""
        buttons = self.page.locator(self.ADD_TO_CART_BUTTON).all()
        if index < len(buttons):
            buttons[index].click()
        return self

    def get_cart_badge_count(self) -> int:
        """장바구니 배지 숫자 반환"""
        if self.is_visible(self.SHOPPING_CART_BADGE, timeout=2000):
            text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(text) if text else 0
        return 0

    def open_menu(self):
        """햄버거 메뉴 열기"""
        self.click(self.BURGER_MENU_BUTTON)
        return self

    def logout(self):
        """로그아웃 수행"""
        self.open_menu()
        # 메뉴 애니메이션 대기
        self.page.wait_for_selector(self.LOGOUT_LINK, state="visible")
        self.click(self.LOGOUT_LINK)
        return self
