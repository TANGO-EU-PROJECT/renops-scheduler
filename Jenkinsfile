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
//         stage('Static Analysis') {
//             parallel {
//                 stage('isort') {
//                     steps {
//                         container('python:3.11.3') {
//                             sh 'pip install isort'
//                             sh 'isort . --check-only'
//                         }
//                     }
//                 }

//                 stage('flake8') {
//                     steps {
//                         container('python:3.11.3') {
//                             sh 'pip install flake8'
//                             sh 'flake8 --max-line-length=120 .'
//                         }
//                     }
//                 }
//             }
//             post {
//                 always {
//                     junit '**/junit-*.xml' // Add this if you generate JUnit reports
//                 }
//             }
//         }

//         stage('Build') {
//             when { branch 'main' } // Execute only on the 'main' branch
//             steps {
//                 script {
//                     def pythonVersion = "python -V"
//                     sh "$pythonVersion"
//                     sh 'pip install virtualenv'
//                     sh 'virtualenv venv'
//                     sh 'source venv/bin/activate'
//                     sh 'pip install build twine'
//                     sh 'python -m build'

//                     // Jenkins Credentials Management
//                     withCredentials([usernamePassword(credentialsId: 'pypi-creds', usernameVariable: 'TWINE_USERNAME', passwordVariable: 'TWINE_PASSWORD')]) { 
//                         sh """
//                            python -m twine upload --verbose --repository-url ${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/pypi dist/* \
//                                   --username ${TWINE_USERNAME} --password ${TWINE_PASSWORD} 
//                         """
//                     } 
//                 }
//             }
//             post {
//                 success {
//                     archiveArtifacts artifacts: 'dist/*.whl', expiresIn: '2 days'
//                 }
//             }
//         }

//         stage('Test') {
//             steps {
//                 script {
//                     // Download your pip package as an artifact 
//                     copyArtifacts projectName: '${JOB_NAME}', selector: specific(file: 'dist/*.whl'), fingerprintArtifacts: true

//                     // Install and test with different Python versions in parallel 
//                     parallel(
//                         "Python 3.8": { 
//                             container('python:3.8.0') { installAndRunTest() } 
//                         },
//                         "Python 3.9": {
//                             container('python:3.9.0') { installAndRunTest() } 
//                         },
//                         // Add more Python versions as needed...
//                         "Python 3.12": {
//                             container('python:3.12.0') { installAndRunTest() } 
//                         }
//                     )
//                 }
//             }
//         }
//     }
// }

// // Reusable function to install and run tests
// def installAndRunTest() {
//     sh 'pip install .'    
//     sh 'pip install pytest'
//     sh 'pytest' 
// }
