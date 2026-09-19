pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'mvn -B clean package -DskipTests'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn -B test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }
        stage('Quality Gate') {
            steps {
                // sonar.qualitygate.wait=true makes this step BLOCK until
                // SonarQube has actually evaluated the gate, and FAIL the
                // build (non-zero exit) if the gate does not pass. Without
                // it, this stage would report success the instant the
                // analysis was merely uploaded - before anyone checked
                // whether it was any good.
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    sh 'mvn -B sonar:sonar -Dsonar.token=$SONAR_TOKEN -Dsonar.qualitygate.wait=true'
                }
            }
        }
        stage('Security Scans') {
            // Three genuinely different blind spots, run in parallel since
            // none of them depend on each other's result: SonarQube (Quality
            // Gate, above) already covers SAST; this stage covers what it
            // doesn't - vulnerable dependencies, and secrets in git history.
            parallel {
                stage('Dependency Check') {
                    steps {
                        sh 'mvn -B dependency:tree'
                        // A real pipeline would call a dedicated scanner
                        // here (e.g. OWASP dependency-check-maven, or a
                        // hosted equivalent) and fail the build on new
                        // CRITICAL/HIGH findings.
                    }
                }
                stage('Secret Scan') {
                    steps {
                        sh 'docker run --rm -v $(pwd):/repo -w /repo zricethezav/gitleaks:latest detect'
                    }
                }
            }
        }
    }
}
