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

    stage('archive') {
      steps {
        archiveArtifacts 'dist/*.tar.gz'
      }
    }

    stage('end') {
      steps {
        echo 'success'
      }
    }

  }
}