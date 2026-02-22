pipeline {
    agent any

    parameters {
        string(
            name: 'TEST_URL',
            defaultValue: 'https://www.saucedemo.com',
            description: '테스트 대상 URL'
        )
    }

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:${env.PATH}"
        DOCKER_IMAGE = 'playwright-test'
        REPORTS_DIR = 'reports'
        TEST_URL = "${params.TEST_URL}"
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Cleanup') {
            steps {
                script {
                    sh '''
                        docker-compose down --remove-orphans || true
                        rm -rf ${REPORTS_DIR}/allure-results ${REPORTS_DIR}/allure-report || true
                        mkdir -p ${REPORTS_DIR}/allure-results
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh 'TEST_URL=${TEST_URL} docker-compose up --abort-on-container-exit --exit-code-from test'
                }
            }
            post {
                always {
                    sh 'docker-compose down --remove-orphans || true'
                }
            }
        }

    }

    post {
        always {
            // Allure Report 발행
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: "${REPORTS_DIR}/allure-results"]]
            ])

            // 아티팩트 보관 (Allure 플러그인이 workspace 루트에 생성)
            archiveArtifacts artifacts: "allure-report/**/*", allowEmptyArchive: true

            // Docker 정리
            sh '''
                docker-compose down --remove-orphans || true
                docker image prune -f || true
            '''

            // Workspace 정리 (선택사항)
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [[pattern: "${REPORTS_DIR}/**", type: 'EXCLUDE']])
        }

        success {
            echo 'Pipeline succeeded! All tests passed.'
        }

        failure {
            echo 'Pipeline failed! Check the test results.'
        }

        unstable {
            echo 'Pipeline unstable! Some tests may have failed.'
        }
    }
}
