# playwright-test

[saucedemo.com](https://www.saucedemo.com) E2E 테스트 자동화 프레임워크입니다.
Playwright + pytest + Page Object Model 패턴으로 구성되며, Docker 컨테이너에서 실행되고 Allure 3로 리포트를 생성합니다.

---

## 기술 스택

| 항목 | 버전 |
|------|------|
| Python | 3.x |
| Playwright | 1.57.0 |
| pytest | 9.0.2 |
| allure-pytest | 2.15.3 |
| Allure CLI | 3.x (전역 설치) |
| Docker | - |

---

## 사전 요구사항

- Docker & Docker Compose
- Node.js (Allure CLI 설치용)
- Allure 3 CLI 전역 설치

```bash
# Allure 3 전역 설치
sudo npm install -g allure

# 설치 확인
allure --version  # 3.x.x
```

---

## 빠른 시작

```bash
# 테스트 실행 + 리포트 생성 + 브라우저에서 열기
./run_test.sh
```

---

## 실행 명령어

### 전체 테스트 실행

```bash
./run_test.sh
```

컨테이너를 내리고 → 리포트 초기화 → 빌드 → 테스트 실행 → Allure 리포트 오픈까지 자동으로 수행합니다.

### 개별 테스트 실행

```bash
# 특정 파일
docker-compose run test pytest tests/test_login.py -v --alluredir=/reports/allure-results

# 특정 클래스
docker-compose run test pytest tests/test_login.py::TestLoginValidUsers -v --alluredir=/reports/allure-results

# 키워드 필터
docker-compose run test pytest -k "checkout" -v --alluredir=/reports/allure-results
```

### Allure 리포트 수동 생성

```bash
# 리포트 생성
allure generate ./reports/allure-results -o ./reports/allure-report

# 브라우저에서 열기 (반드시 allure open 사용 — 직접 index.html 열면 ??? 로 표시됨)
allure open ./reports/allure-report
```

### 리포트 데이터 초기화

```bash
./reset.sh
```

---

## 프로젝트 구조

```
playwright-test/
├── pages/                    # Page Object Model
│   ├── base_page.py          # 공통 Playwright 래퍼
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── product_detail_page.py
│   └── checkout_page.py      # Step1 / Step2 / Complete
├── tests/                    # 테스트 파일
│   ├── test_login.py         # 로그인 테스트
│   ├── test_inventory.py     # 상품 목록 테스트
│   ├── test_product_detail.py
│   ├── test_cart.py
│   └── test_checkout.py
├── data/
│   └── users.py              # 테스트 사용자 데이터
├── utils/
│   └── config.py             # 환경변수 기반 설정
├── docs/
│   └── JENKINS_SETUP.md      # Jenkins 설정 가이드
├── conftest.py               # pytest fixture & 테스트 순서
├── pytest.ini
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── run_test.sh               # 메인 실행 스크립트
└── reset.sh                  # 리포트 데이터 초기화
```

---

## 테스트 구성

### 테스트 실행 순서

`conftest.py`의 `TEST_ORDER`에 따라 아래 순서로 실행됩니다.

```
test_login → test_inventory → test_product_detail → test_cart → test_checkout
```

### 테스트 사용자

saucedemo.com에서 제공하는 6종 사용자 타입을 `data/users.py`에 정의합니다.

| 사용자명 | 설명 |
|---------|------|
| `standard_user` | 정상 사용자 |
| `locked_out_user` | 로그인 불가 (잠긴 계정) |
| `problem_user` | 이미지 깨짐 등 버그 발생 |
| `performance_glitch_user` | 응답 지연 |
| `error_user` | 특정 기능에서 에러 발생 |
| `visual_user` | UI 렌더링 버그 |

공통 패스워드: `secret_sauce`

### 주요 fixture

| fixture | 설명 |
|---------|------|
| `login_page` | 로그인 페이지 열기 |
| `logged_in_page` | standard_user로 로그인된 InventoryPage |
| `logged_in_with_cart` | 로그인 + 장바구니에 2개 상품 추가된 상태 |
| `capture_screenshot` | 모든 테스트 종료 시 스크린샷 자동 첨부 (autouse) |

---

## 환경변수

`docker-compose.yml` 또는 실행 시 환경변수로 설정합니다.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DEFAULT_TIMEOUT` | `10` | 요소 대기 타임아웃 (초) |
| `PAGE_LOAD_TIMEOUT` | `30` | 페이지 로드 타임아웃 (초) |
| `HEADLESS` | `true` | 헤드리스 모드 여부 |
| `BROWSER` | `chromium` | 브라우저 종류 (chromium / firefox / webkit) |

---

## CI/CD (Jenkins)

Jenkins 파이프라인은 `Jenkinsfile`에 정의되어 있습니다.

```
Cleanup → Build → Test → Allure 리포트 발행 → 아티팩트 저장
```

상세 설정은 [docs/JENKINS_SETUP.md](docs/JENKINS_SETUP.md)를 참고하세요.
