pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps { echo 'Checking out...' }
    }
    stage('Unit Tests') {
      steps {
        echo 'Run pytest'
        bat 'pytest -q'
      }
    }
    stage('Build & Package') {
      steps {
        echo 'Build steps would go here (wheel, docker, etc)'
      }
    }
  }
}
