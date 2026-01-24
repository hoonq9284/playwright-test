import pytest
import allure
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# 테스트 모듈 실행 순서 정의
TEST_ORDER = [
    "test_login",      # 1순위: 로그인 테스트
    "test_inventory",  # 2순위: 인벤토리 테스트
]


def pytest_collection_modifyitems(items):
    """테스트 실행 순서를 TEST_ORDER에 따라 정렬"""
    def get_order(item):
        # 모듈 이름에서 순서 결정
        module_name = item.module.__name__.split(".")[-1]
        try:
            return TEST_ORDER.index(module_name)
        except ValueError:
            return len(TEST_ORDER)  # 목록에 없으면 마지막에 실행

    items.sort(key=get_order)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 결과를 fixture에서 접근할 수 있도록 저장"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def login_page(page: Page):
    """LoginPage 인스턴스 반환"""
    login = LoginPage(page)
    login.open()
    return login


@pytest.fixture
def inventory_page(page: Page):
    """InventoryPage 인스턴스 반환"""
    return InventoryPage(page)


@pytest.fixture
def logged_in_page(page: Page):
    """표준 사용자로 로그인된 상태의 InventoryPage 반환"""
    from data.users import Users
    login = LoginPage(page)
    login.open()
    login.login(Users.STANDARD.username, Users.STANDARD.password)
    return InventoryPage(page)


@pytest.fixture(autouse=True)
def capture_screenshot(request, page: Page):
    """모든 테스트에서 스크린샷 첨부"""
    yield
    # 테스트 완료 후 항상 스크린샷 저장
    status = "passed"
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        status = "failed"

    allure.attach(
        page.screenshot(full_page=True),
        name=f"screenshot_{status}",
        attachment_type=allure.attachment_type.PNG
    )
