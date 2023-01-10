pipeline {
	agent any

	stages {
		stage('Execute Testing') {
			steps {
                sh 'pip install -r requirements.txt'
				sh 'python3 main.py'
			}
		}
	}
}