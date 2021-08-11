pipeline {
  agent {
    docker {
      image 'python:3.7'
    }

  }
  stages {
    stage('build') {
      steps {
        sh 'python setup.py sdist'
      }
    }

    stage('') {
      steps {
        archiveArtifacts 'dist/*.tar.gz'
      }
    }

  }
}