pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'playwright-test'
        REPORTS_DIR = 'reports'
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
                    sh 'docker-compose up --abort-on-container-exit --exit-code-from test'
                }
            }
            post {
                always {
                    sh 'docker-compose down --remove-orphans || true'
                }
            }
        }

        stage('Generate Report') {
            steps {
                script {
                    sh '''
                        if [ -d "${REPORTS_DIR}/allure-results" ] && [ "$(ls -A ${REPORTS_DIR}/allure-results)" ]; then
                            echo "Generating Allure report..."
                            allure generate ${REPORTS_DIR}/allure-results -o ${REPORTS_DIR}/allure-report --clean
                        else
                            echo "No test results found!"
                            exit 1
                        fi
                    '''
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

            // 아티팩트 보관
            archiveArtifacts artifacts: "${REPORTS_DIR}/allure-report/**/*", allowEmptyArchive: true

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
