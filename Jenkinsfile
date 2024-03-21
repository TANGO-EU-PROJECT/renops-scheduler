pipeline {
    agent {
        node {
            label 'Agent01'
        }
    }
    options {
        // Ensures job runs to completion even with minor non-fatal errors 
        skipDefaultCheckout() 
    }

    environment {
        BRANCH_NAME = "main"
    }

    stages {
        
        stage('Checkout') {
          steps {
              echo 'Checkout SCM'
              checkout scm
            }
        }

        stage("Build"){
            steps{
                script {
                    echo "Building"
                    sh "ls -all"
                    sh "python -V"
                    sh "pip install virtualenv"
                    sh "virtualenv venv"
                    sh "source venv/bin/activate"
                    sh "pip install build"
                    sh "python -m build"
                }
            }
        }

        stage("Test"){
            environment {
                RENOPSAPI_KEY = credentials('RENOPSAPI_KEY')
            }
            steps {
                script {
                    echo "Testing"
                    sh "pip install ."
                    sh 'pip install pytest'
                    sh 'python -m pytest'
                }
            }
        
        }
    }
}
