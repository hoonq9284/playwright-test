# Jenkins CI/CD 설정 가이드

## 필수 요구사항

### Jenkins 플러그인
Jenkins 관리 > 플러그인 관리에서 다음 플러그인을 설치하세요:

| 플러그인 | 용도 |
|---------|------|
| Docker Pipeline | Docker 명령어 실행 |
| Docker Compose Build Step | docker-compose 지원 |
| Allure | Allure 리포트 발행 |
| Pipeline | Pipeline 스크립트 지원 |
| Git | Git 저장소 연동 |

### Jenkins 서버 요구사항
- Docker 설치
- Docker Compose 설치
- Allure CLI 설치

```bash
# Allure CLI 설치 (Ubuntu/Debian)
sudo apt-get install allure

# Allure CLI 설치 (macOS)
brew install allure
```

---

## Jenkins Job 생성

### 1. 새 Item 생성
1. Jenkins 대시보드 > **New Item**
2. 이름 입력: `playwright-e2e-tests`
3. **Pipeline** 선택 > OK

### 2. Pipeline 설정

#### General
- [x] Do not allow concurrent builds
- [x] GitHub project (선택사항)

#### Build Triggers (선택)
```
# 정기 실행 (매일 오전 9시)
H 9 * * *

# 또는 Git Push 시 실행
GitHub hook trigger for GITScm polling
```

#### Pipeline
- Definition: **Pipeline script from SCM**
- SCM: **Git**
- Repository URL: `https://github.com/hoonq9284/playwright-test.git`
- Branch: `*/main`
- Script Path: `Jenkinsfile`

---

## Allure 설정

### Jenkins에서 Allure 도구 설정
1. Jenkins 관리 > Tool
2. **Allure Commandline Installation** 섹션
3. Add Allure Commandline
   - Name: `allure`
   - Install automatically 체크
   - Version: 최신 버전 선택

---

## 환경 변수 설정 (선택사항)

Jenkins 관리 > System > Global properties에서 환경 변수 추가:

| 변수명 | 값 | 설명 |
|-------|-----|------|
| DEFAULT_TIMEOUT | 10 | 기본 타임아웃 (초) |
| PAGE_LOAD_TIMEOUT | 30 | 페이지 로드 타임아웃 (초) |
| HEADLESS | true | 헤드리스 모드 |

---

## 파이프라인 실행 흐름

```
┌─────────────┐
│   Cleanup   │  이전 컨테이너/리포트 정리
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Build    │  Docker 이미지 빌드
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Test     │  Playwright 테스트 실행
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Report    │  Allure 리포트 생성
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Publish   │  Allure 리포트 발행 & 아티팩트 저장
└─────────────┘
```

---

## 트러블슈팅

### Docker 권한 오류
```bash
# Jenkins 사용자를 docker 그룹에 추가
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Allure 명령어를 찾을 수 없음
```bash
# Jenkins 노드에서 Allure 경로 확인
which allure

# Jenkinsfile에서 전체 경로 사용
/usr/local/bin/allure generate ...
```

### 테스트 결과가 없음
- `reports/allure-results` 디렉토리 권한 확인
- Docker 볼륨 마운트 확인
- docker-compose.yml의 volumes 설정 확인

---

## Webhook 설정 (GitHub)

### GitHub에서 Jenkins Webhook 추가
1. GitHub 저장소 > Settings > Webhooks
2. Add webhook
   - Payload URL: `http://your-jenkins-url/github-webhook/`
   - Content type: `application/json`
   - Events: `Just the push event`

---

## 알림 설정 (선택사항)

### Slack 알림
```groovy
// Jenkinsfile post 섹션에 추가
post {
    failure {
        slackSend(
            channel: '#ci-alerts',
            color: 'danger',
            message: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        )
    }
}
```

### 이메일 알림
```groovy
post {
    failure {
        emailext(
            subject: "Build Failed: ${env.JOB_NAME}",
            body: "Check console output: ${env.BUILD_URL}",
            recipientProviders: [developers()]
        )
    }
}
```
