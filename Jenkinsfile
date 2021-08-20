pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh 'python setup.py sdist'
      }
    }

    stage('archive') {
      steps {
        archiveArtifacts '**/*.tar.gz'
      }
    }

    stage('end') {
      steps {
        echo 'success'
      }
    }

  }
}