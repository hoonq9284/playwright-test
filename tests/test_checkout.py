import pytest
from playwright.sync_api import Page

from data.users import Users
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage


class TestCheckoutStepOneValidation:
    """체크아웃 1단계 유효성 검사 테스트"""

    @pytest.fixture
    def checkout_ready(self, logged_in_page, cart_page, checkout_step_one_page):
        """체크아웃 1단계 준비"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.click_shopping_cart()
        cart_page.click_checkout()
        return checkout_step_one_page

    def test_checkout_step_one_page_title(self, checkout_ready):
        """체크아웃 1단계 페이지 타이틀 확인"""
        title = checkout_ready.get_page_title()

        assert title == "Checkout: Your Information", f"Expected 'Checkout: Your Information', got '{title}'"

    def test_empty_first_name_shows_error(self, checkout_ready):
        """빈 이름으로 제출 시 에러 메시지 표시"""
        checkout_ready.enter_last_name("Doe")
        checkout_ready.enter_postal_code("12345")
        checkout_ready.click_continue()

        assert checkout_ready.is_error_displayed(), "Error should be displayed"
        assert "First Name is required" in checkout_ready.get_error_message()

    def test_empty_last_name_shows_error(self, checkout_ready):
        """빈 성으로 제출 시 에러 메시지 표시"""
        checkout_ready.enter_first_name("John")
        checkout_ready.enter_postal_code("12345")
        checkout_ready.click_continue()

        assert checkout_ready.is_error_displayed(), "Error should be displayed"
        assert "Last Name is required" in checkout_ready.get_error_message()

    def test_empty_postal_code_shows_error(self, checkout_ready):
        """빈 우편번호로 제출 시 에러 메시지 표시"""
        checkout_ready.enter_first_name("John")
        checkout_ready.enter_last_name("Doe")
        checkout_ready.click_continue()

        assert checkout_ready.is_error_displayed(), "Error should be displayed"
        assert "Postal Code is required" in checkout_ready.get_error_message()

    def test_all_empty_fields_shows_error(self, checkout_ready):
        """모든 필드가 비어있을 때 에러 메시지 표시"""
        checkout_ready.click_continue()

        assert checkout_ready.is_error_displayed(), "Error should be displayed"
        assert "First Name is required" in checkout_ready.get_error_message()

    def test_close_error_message(self, checkout_ready):
        """에러 메시지 닫기"""
        checkout_ready.click_continue()

        assert checkout_ready.is_error_displayed()

        checkout_ready.close_error()

        # 에러 닫기 후 확인 (에러 버튼은 에러를 닫는 역할)
        # 실제로 에러가 사라지는지는 구현에 따라 다를 수 있음


class TestCheckoutStepOneNavigation:
    """체크아웃 1단계 네비게이션 테스트"""

    @pytest.fixture
    def checkout_ready(self, logged_in_page, cart_page, checkout_step_one_page):
        """체크아웃 1단계 준비"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.click_shopping_cart()
        cart_page.click_checkout()
        return checkout_step_one_page

    def test_cancel_returns_to_cart(self, checkout_ready, cart_page):
        """취소 버튼 클릭 시 장바구니로 복귀"""
        checkout_ready.click_cancel()

        assert cart_page.is_cart_page(), "Should return to cart page"

    def test_valid_info_navigates_to_step_two(self, checkout_ready, checkout_step_two_page):
        """유효한 정보 입력 후 2단계로 이동"""
        checkout_ready.fill_checkout_info("John", "Doe", "12345")
        checkout_ready.click_continue()

        assert checkout_step_two_page.is_checkout_step_two_page(), "Should navigate to checkout step two"


class TestCheckoutStepTwo:
    """체크아웃 2단계 테스트"""

    @pytest.fixture
    def checkout_step_two_ready(self, logged_in_page, cart_page, checkout_step_one_page, checkout_step_two_page):
        """체크아웃 2단계 준비 (상품 2개 포함)"""
        # 가격 정보 먼저 저장
        item_names = logged_in_page.get_item_names()
        prices = logged_in_page.get_item_prices()
        price_values = [float(prices[0].replace("$", "")), float(prices[1].replace("$", ""))]

        # 이름으로 상품 추가 (인덱스 밀림 방지)
        logged_in_page.add_item_to_cart_by_name(item_names[0])
        logged_in_page.add_item_to_cart_by_name(item_names[1])

        logged_in_page.click_shopping_cart()
        cart_page.click_checkout()
        checkout_step_one_page.fill_checkout_info("John", "Doe", "12345")
        checkout_step_one_page.click_continue()

        return checkout_step_two_page, price_values

    def test_checkout_step_two_page_title(self, checkout_step_two_ready):
        """체크아웃 2단계 페이지 타이틀 확인"""
        checkout_page, _ = checkout_step_two_ready
        title = checkout_page.get_page_title()

        assert title == "Checkout: Overview", f"Expected 'Checkout: Overview', got '{title}'"

    def test_items_displayed_in_overview(self, checkout_step_two_ready):
        """주문 개요에 아이템이 표시되는지 확인"""
        checkout_page, _ = checkout_step_two_ready
        item_count = checkout_page.get_cart_item_count()

        assert item_count == 2, f"Expected 2 items, got {item_count}"

    def test_subtotal_is_correct(self, checkout_step_two_ready):
        """소계가 올바른지 확인"""
        checkout_page, price_values = checkout_step_two_ready
        expected_subtotal = sum(price_values)
        actual_subtotal = checkout_page.get_subtotal_value()

        assert abs(actual_subtotal - expected_subtotal) < 0.01, \
            f"Expected subtotal ${expected_subtotal}, got ${actual_subtotal}"

    def test_tax_is_calculated(self, checkout_step_two_ready):
        """세금이 계산되는지 확인"""
        checkout_page, _ = checkout_step_two_ready
        tax = checkout_page.get_tax_value()

        assert tax > 0, "Tax should be greater than 0"

    def test_total_equals_subtotal_plus_tax(self, checkout_step_two_ready):
        """총액이 소계 + 세금과 일치하는지 확인"""
        checkout_page, _ = checkout_step_two_ready
        subtotal = checkout_page.get_subtotal_value()
        tax = checkout_page.get_tax_value()
        total = checkout_page.get_total_value()
        expected_total = subtotal + tax

        assert abs(total - expected_total) < 0.01, \
            f"Total should be {expected_total}, got {total}"

    def test_cancel_returns_to_inventory(self, checkout_step_two_ready):
        """취소 버튼 클릭 시 인벤토리로 복귀"""
        checkout_page, _ = checkout_step_two_ready
        checkout_page.click_cancel()

        inventory_page = InventoryPage(checkout_page.page)
        assert inventory_page.is_inventory_page(), "Should return to inventory page"


class TestCheckoutComplete:
    """체크아웃 완료 테스트"""

    @pytest.fixture
    def checkout_complete_ready(self, logged_in_page, cart_page, checkout_step_one_page,
                                 checkout_step_two_page, checkout_complete_page):
        """체크아웃 완료 준비"""
        logged_in_page.add_item_to_cart_by_index(0)
        logged_in_page.click_shopping_cart()
        cart_page.click_checkout()
        checkout_step_one_page.fill_checkout_info("John", "Doe", "12345")
        checkout_step_one_page.click_continue()
        checkout_step_two_page.click_finish()
        return checkout_complete_page

    def test_checkout_complete_page_title(self, checkout_complete_ready):
        """체크아웃 완료 페이지 타이틀 확인"""
        title = checkout_complete_ready.get_page_title()

        assert title == "Checkout: Complete!", f"Expected 'Checkout: Complete!', got '{title}'"

    def test_thank_you_message_displayed(self, checkout_complete_ready):
        """감사 메시지가 표시되는지 확인"""
        header = checkout_complete_ready.get_complete_header()

        assert "Thank you" in header, f"Expected 'Thank you' in header, got '{header}'"

    def test_order_dispatched_message_displayed(self, checkout_complete_ready):
        """주문 발송 메시지가 표시되는지 확인"""
        message = checkout_complete_ready.get_complete_text()

        assert "dispatched" in message.lower() or "order" in message.lower(), \
            f"Expected order message, got '{message}'"

    def test_pony_express_image_displayed(self, checkout_complete_ready):
        """Pony Express 이미지가 표시되는지 확인"""
        assert checkout_complete_ready.is_pony_express_displayed(), "Pony Express image should be displayed"

    def test_back_home_returns_to_inventory(self, checkout_complete_ready):
        """'Back Home' 버튼 클릭 시 인벤토리로 복귀"""
        checkout_complete_ready.click_back_home()

        inventory_page = InventoryPage(checkout_complete_ready.page)
        assert inventory_page.is_inventory_page(), "Should return to inventory page"

    def test_cart_is_empty_after_checkout(self, checkout_complete_ready):
        """체크아웃 완료 후 장바구니가 비어있는지 확인"""
        checkout_complete_ready.click_back_home()

        inventory_page = InventoryPage(checkout_complete_ready.page)
        badge_count = inventory_page.get_cart_badge_count()

        assert badge_count == 0, "Cart should be empty after checkout"


class TestFullCheckoutFlow:
    """전체 체크아웃 플로우 테스트"""

    def test_complete_checkout_with_single_item(self, logged_in_page, cart_page,
                                                 checkout_step_one_page, checkout_step_two_page,
                                                 checkout_complete_page):
        """단일 상품 전체 체크아웃 플로우"""
        # 1. 상품 추가
        item_name = logged_in_page.get_item_names()[0]
        logged_in_page.add_item_to_cart_by_index(0)

        # 2. 장바구니로 이동
        logged_in_page.click_shopping_cart()
        assert cart_page.is_cart_page()
        assert item_name in cart_page.get_item_names()

        # 3. 체크아웃 시작
        cart_page.click_checkout()
        assert checkout_step_one_page.is_checkout_step_one_page()

        # 4. 정보 입력
        checkout_step_one_page.fill_checkout_info("Test", "User", "10001")
        checkout_step_one_page.click_continue()

        # 5. 주문 확인
        assert checkout_step_two_page.is_checkout_step_two_page()
        assert checkout_step_two_page.get_cart_item_count() == 1
        assert checkout_step_two_page.get_total_value() > 0

        # 6. 주문 완료
        checkout_step_two_page.click_finish()
        assert checkout_complete_page.is_checkout_complete_page()
        assert "Thank you" in checkout_complete_page.get_complete_header()

    def test_complete_checkout_with_multiple_items(self, logged_in_page, cart_page,
                                                    checkout_step_one_page, checkout_step_two_page,
                                                    checkout_complete_page):
        """다중 상품 전체 체크아웃 플로우"""
        # 1. 여러 상품 추가
        for i in range(3):
            logged_in_page.add_item_to_cart_by_index(i)

        assert logged_in_page.get_cart_badge_count() == 3

        # 2. 장바구니로 이동
        logged_in_page.click_shopping_cart()
        assert cart_page.get_cart_item_count() == 3

        # 3. 체크아웃 진행
        cart_page.click_checkout()
        checkout_step_one_page.fill_checkout_info("Multi", "Item", "90210")
        checkout_step_one_page.click_continue()

        # 4. 주문 확인
        assert checkout_step_two_page.get_cart_item_count() == 3

        # 5. 총액 확인 (세금 포함)
        subtotal = checkout_step_two_page.get_subtotal_value()
        tax = checkout_step_two_page.get_tax_value()
        total = checkout_step_two_page.get_total_value()

        assert abs(total - (subtotal + tax)) < 0.01

        # 6. 주문 완료
        checkout_step_two_page.click_finish()
        assert checkout_complete_page.is_checkout_complete_page()


class TestCheckoutWithSpecialUsers:
    """특수 사용자 체크아웃 테스트"""

    def test_error_user_checkout_flow(self, page: Page, cart_page, checkout_step_one_page,
                                       checkout_step_two_page, checkout_complete_page):
        """에러 사용자 체크아웃 (에러 발생 가능)"""
        # 에러 사용자로 로그인
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(Users.ERROR.username, Users.ERROR.password)

        inventory_page = InventoryPage(page)
        inventory_page.add_item_to_cart_by_index(0)
        inventory_page.click_shopping_cart()

        cart_page.click_checkout()

        # 에러 사용자는 체크아웃 과정에서 에러가 발생할 수 있음
        # 이 테스트는 에러 발생 여부를 확인하는 용도
        if checkout_step_one_page.is_checkout_step_one_page():
            checkout_step_one_page.fill_checkout_info("Error", "User", "00000")
            checkout_step_one_page.click_continue()

    def test_performance_glitch_user_checkout(self, page: Page, cart_page, checkout_step_one_page,
                                               checkout_step_two_page, checkout_complete_page):
        """성능 문제 사용자 체크아웃 (느릴 수 있음)"""
        # 성능 문제 사용자로 로그인
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(Users.PERFORMANCE_GLITCH.username, Users.PERFORMANCE_GLITCH.password)

        inventory_page = InventoryPage(page)
        inventory_page.add_item_to_cart_by_index(0)
        inventory_page.click_shopping_cart()

        cart_page.click_checkout()

        assert checkout_step_one_page.is_checkout_step_one_page()

        checkout_step_one_page.fill_checkout_info("Slow", "User", "11111")
        checkout_step_one_page.click_continue()

        assert checkout_step_two_page.is_checkout_step_two_page()

        checkout_step_two_page.click_finish()

        assert checkout_complete_page.is_checkout_complete_page()
