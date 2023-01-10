pipeline {
	agent any

	stages {
        stage('Install Modules'){
            steps{
                sh 'pip install -r requirements.txt'
            }
        }
		stage('Execute Testing') {
			steps {
				sh 'python3 main.py'
			}
		}
        stage('View Logs'){
            steps{
                sh 'cat logs.log'
            }
        }
	}
}