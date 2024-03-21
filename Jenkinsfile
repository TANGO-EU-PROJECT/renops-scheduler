def runTest() {
    sh '''
        pip install renops-scheduler
        echo 'print("hello world!")' > test.py
        renops-scheduler test.py -la -r 1 -d 1 --optimise-price # Test prices
    ''' 
}

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
        timeout(time: 20, unit: 'MINUTES')    
        // Create credentials in Jenkins for security
        TWINE_PASSWORD = credentials('pypi-token')
        RENOPSAPI_KEY = credentials('RENOPSAPI_KEY')
        TWINE_USERNAME = "__token__" 
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

        stage('Publish') {
            steps {
                sh '''
                    python -m twine upload --verbose --repository-url https://upload.pypi.org/legacy/ dist/* 
                '''
            }
        } 
        stage('Test') {
            parallel {
                stage('Python 3.8') {
                    agent { label 'python-3.8' } 
                    steps {
                        runTest() 
                    }
                }
                stage('Python 3.9') {
                    agent { label 'python-3.9' } 
                    steps {
                        runTest() 
                    }
                }
                stage('Python 3.9') {
                    agent { label 'python-3.10' } 
                    steps {
                        runTest() 
                    }
                }
                stage('Python 3.11') {
                    agent { label 'python-3.11' } 
                    steps {
                        runTest() 
                    }
                }
                
        }
        // Reusable function 
        
        }   
    }
}
