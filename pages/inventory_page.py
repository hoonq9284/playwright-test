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
    INVENTORY_ITEM_IMAGE = ".inventory_item_img"
    ADD_TO_CART_BUTTON = "button[data-test^='add-to-cart']"
    REMOVE_BUTTON = "button[data-test^='remove']"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    CLOSE_MENU_BUTTON = "#react-burger-cross-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    ALL_ITEMS_LINK = "#inventory_sidebar_link"
    ABOUT_LINK = "#about_sidebar_link"
    RESET_APP_LINK = "#reset_sidebar_link"
    SORT_DROPDOWN = ".product_sort_container"
    FOOTER = ".footer"
    TWITTER_LINK = ".social_twitter a"
    FACEBOOK_LINK = ".social_facebook a"
    LINKEDIN_LINK = ".social_linkedin a"

    # Sort options
    SORT_AZ = "az"
    SORT_ZA = "za"
    SORT_LOHI = "lohi"
    SORT_HILO = "hilo"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{Config.BASE_URL}/inventory.html"

    def is_inventory_page(self) -> bool:
        """현재 페이지가 인벤토리 페이지인지 확인"""
        return self.is_visible(self.INVENTORY_LIST, timeout=5000)

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

    def open_menu(self):
        """햄버거 메뉴 열기"""
        self.click(self.BURGER_MENU_BUTTON)
        return self

    def logout(self):
        """로그아웃 수행"""
        self.open_menu()
        self.page.wait_for_selector(self.LOGOUT_LINK, state="visible")
        self.click(self.LOGOUT_LINK)
        return self

    def close_menu(self):
        """햄버거 메뉴 닫기"""
        self.click(self.CLOSE_MENU_BUTTON)
        self.page.wait_for_selector(self.CLOSE_MENU_BUTTON, state="hidden")
        return self

    def click_all_items(self):
        """전체 아이템 메뉴 클릭"""
        self.open_menu()
        self.page.wait_for_selector(self.ALL_ITEMS_LINK, state="visible")
        self.click(self.ALL_ITEMS_LINK)
        return self

    def click_about(self):
        """About 메뉴 클릭"""
        self.open_menu()
        self.page.wait_for_selector(self.ABOUT_LINK, state="visible")
        self.click(self.ABOUT_LINK)
        return self

    def reset_app_state(self):
        """앱 상태 초기화"""
        self.open_menu()
        self.page.wait_for_selector(self.RESET_APP_LINK, state="visible")
        self.click(self.RESET_APP_LINK)
        return self

    def sort_by(self, sort_option: str):
        """정렬 옵션 선택 (az, za, lohi, hilo)"""
        self.page.select_option(self.SORT_DROPDOWN, sort_option)
        return self

    def sort_by_name_asc(self):
        """이름 오름차순 정렬 (A to Z)"""
        return self.sort_by(self.SORT_AZ)

    def sort_by_name_desc(self):
        """이름 내림차순 정렬 (Z to A)"""
        return self.sort_by(self.SORT_ZA)

    def sort_by_price_asc(self):
        """가격 오름차순 정렬 (Low to High)"""
        return self.sort_by(self.SORT_LOHI)

    def sort_by_price_desc(self):
        """가격 내림차순 정렬 (High to Low)"""
        return self.sort_by(self.SORT_HILO)

    def get_current_sort_option(self) -> str:
        """현재 정렬 옵션 반환"""
        return self.page.locator(self.SORT_DROPDOWN).input_value()

    def get_item_prices_as_float(self) -> list[float]:
        """모든 아이템 가격을 숫자로 반환"""
        prices = self.get_item_prices()
        return [float(p.replace("$", "")) for p in prices]

    def click_product_by_name(self, product_name: str):
        """상품 이름으로 상품 상세 페이지 이동"""
        self.page.locator(self.INVENTORY_ITEM_NAME, has_text=product_name).click()
        return self

    def click_product_by_index(self, index: int = 0):
        """인덱스로 상품 상세 페이지 이동"""
        items = self.page.locator(self.INVENTORY_ITEM_NAME).all()
        if index < len(items):
            items[index].click()
        return self

    def click_product_image_by_index(self, index: int = 0):
        """이미지 클릭으로 상품 상세 페이지 이동"""
        images = self.page.locator(self.INVENTORY_ITEM_IMAGE).all()
        if index < len(images):
            images[index].click()
        return self

    def add_item_to_cart_by_name(self, item_name: str):
        """이름으로 아이템을 장바구니에 추가"""
        add_button = f"[data-test='add-to-cart-{self._item_name_to_id(item_name)}']"
        if self.is_visible(add_button, timeout=2000):
            self.click(add_button)
        return self

    def remove_item_from_cart_by_name(self, item_name: str):
        """이름으로 아이템을 장바구니에서 제거"""
        remove_button = f"[data-test='remove-{self._item_name_to_id(item_name)}']"
        if self.is_visible(remove_button, timeout=2000):
            self.click(remove_button)
        return self

    def remove_item_from_cart_by_index(self, index: int = 0):
        """인덱스로 아이템을 장바구니에서 제거"""
        buttons = self.page.locator(self.REMOVE_BUTTON).all()
        if index < len(buttons):
            buttons[index].click()
        return self

    def get_add_to_cart_button_count(self) -> int:
        """Add to cart 버튼 개수 반환"""
        return self.get_element_count(self.ADD_TO_CART_BUTTON)

    def get_remove_button_count(self) -> int:
        """Remove 버튼 개수 반환"""
        return self.get_element_count(self.REMOVE_BUTTON)

    def click_shopping_cart(self):
        """장바구니 아이콘 클릭"""
        self.click(self.SHOPPING_CART_LINK)
        return self

    def get_item_descriptions(self) -> list[str]:
        """모든 아이템 설명 반환"""
        elements = self.page.locator(self.INVENTORY_ITEM_DESC).all()
        return [el.text_content() or "" for el in elements]

    def is_footer_visible(self) -> bool:
        """푸터가 표시되는지 확인"""
        return self.is_visible(self.FOOTER, timeout=3000)

    def get_twitter_link(self) -> str:
        """Twitter 링크 반환"""
        return self.page.locator(self.TWITTER_LINK).get_attribute("href") or ""

    def get_facebook_link(self) -> str:
        """Facebook 링크 반환"""
        return self.page.locator(self.FACEBOOK_LINK).get_attribute("href") or ""

    def get_linkedin_link(self) -> str:
        """LinkedIn 링크 반환"""
        return self.page.locator(self.LINKEDIN_LINK).get_attribute("href") or ""
