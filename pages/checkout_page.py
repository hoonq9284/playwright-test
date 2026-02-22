from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.config import Config


class CheckoutStepOnePage(BasePage):
    """체크아웃 1단계 - 정보 입력 페이지"""

    # Selectors
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_BUTTON = ".error-button"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{Config.BASE_URL}/checkout-step-one.html"

    def is_checkout_step_one_page(self) -> bool:
        """현재 페이지가 체크아웃 1단계인지 확인"""
        return self.is_visible(self.FIRST_NAME_INPUT, timeout=5000)

    def enter_first_name(self, first_name: str):
        """이름 입력"""
        self.fill(self.FIRST_NAME_INPUT, first_name)
        return self

    def enter_last_name(self, last_name: str):
        """성 입력"""
        self.fill(self.LAST_NAME_INPUT, last_name)
        return self

    def enter_postal_code(self, postal_code: str):
        """우편번호 입력"""
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        """체크아웃 정보 모두 입력"""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self

    def click_continue(self):
        """계속 버튼 클릭"""
        self.click(self.CONTINUE_BUTTON)
        return self

    def click_cancel(self):
        """취소 버튼 클릭"""
        self.click(self.CANCEL_BUTTON)
        return self

    def is_error_displayed(self) -> bool:
        """에러 메시지가 표시되는지 확인"""
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)

    def get_error_message(self) -> str:
        """에러 메시지 텍스트 반환"""
        return self.get_text(self.ERROR_MESSAGE)

    def close_error(self):
        """에러 메시지 닫기"""
        self.click(self.ERROR_BUTTON)
        return self


class CheckoutStepTwoPage(BasePage):
    """체크아웃 2단계 - 주문 확인 페이지"""

    # Selectors
    CART_LIST = ".cart_list"
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    CART_ITEM_QUANTITY = ".cart_quantity"
    SUMMARY_INFO = ".summary_info"
    SUMMARY_SUBTOTAL = ".summary_subtotal_label"
    SUMMARY_TAX = ".summary_tax_label"
    SUMMARY_TOTAL = ".summary_total_label"
    PAYMENT_INFO = ".summary_value_label"
    FINISH_BUTTON = "[data-test='finish']"
    CANCEL_BUTTON = "[data-test='cancel']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{Config.BASE_URL}/checkout-step-two.html"

    def is_checkout_step_two_page(self) -> bool:
        """현재 페이지가 체크아웃 2단계인지 확인"""
        return self.is_visible(self.SUMMARY_INFO, timeout=5000)

    def get_cart_item_count(self) -> int:
        """장바구니 아이템 개수 반환"""
        return self.get_element_count(self.CART_ITEM)

    def get_item_names(self) -> list[str]:
        """모든 아이템 이름 반환"""
        elements = self.page.locator(self.CART_ITEM_NAME).all()
        return [el.text_content() or "" for el in elements]

    def get_item_prices(self) -> list[str]:
        """모든 아이템 가격 반환"""
        elements = self.page.locator(self.CART_ITEM_PRICE).all()
        return [el.text_content() or "" for el in elements]

    def get_subtotal(self) -> str:
        """소계 반환"""
        text = self.get_text(self.SUMMARY_SUBTOTAL)
        return text.replace("Item total: ", "") if text else ""

    def get_tax(self) -> str:
        """세금 반환"""
        text = self.get_text(self.SUMMARY_TAX)
        return text.replace("Tax: ", "") if text else ""

    def get_total(self) -> str:
        """총액 반환"""
        text = self.get_text(self.SUMMARY_TOTAL)
        return text.replace("Total: ", "") if text else ""

    def get_subtotal_value(self) -> float:
        """소계 숫자 값 반환"""
        subtotal = self.get_subtotal()
        return float(subtotal.replace("$", "")) if subtotal else 0.0

    def get_tax_value(self) -> float:
        """세금 숫자 값 반환"""
        tax = self.get_tax()
        return float(tax.replace("$", "")) if tax else 0.0

    def get_total_value(self) -> float:
        """총액 숫자 값 반환"""
        total = self.get_total()
        return float(total.replace("$", "")) if total else 0.0

    def click_finish(self):
        """완료 버튼 클릭"""
        self.click(self.FINISH_BUTTON)
        return self

    def click_cancel(self):
        """취소 버튼 클릭"""
        self.click(self.CANCEL_BUTTON)
        return self


class CheckoutCompletePage(BasePage):
    """체크아웃 완료 페이지"""

    # Selectors
    COMPLETE_CONTAINER = ".checkout_complete_container"
    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    PONY_EXPRESS_IMAGE = ".pony_express"
    BACK_HOME_BUTTON = "[data-test='back-to-products']"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{Config.BASE_URL}/checkout-complete.html"

    def is_checkout_complete_page(self) -> bool:
        """현재 페이지가 체크아웃 완료 페이지인지 확인"""
        return self.is_visible(self.COMPLETE_CONTAINER, timeout=5000)

    def get_complete_header(self) -> str:
        """완료 헤더 텍스트 반환"""
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        """완료 메시지 텍스트 반환"""
        return self.get_text(self.COMPLETE_TEXT)

    def is_pony_express_displayed(self) -> bool:
        """Pony Express 이미지가 표시되는지 확인"""
        return self.is_visible(self.PONY_EXPRESS_IMAGE, timeout=3000)

    def click_back_home(self):
        """홈으로 돌아가기 버튼 클릭"""
        self.click(self.BACK_HOME_BUTTON)
        return self
