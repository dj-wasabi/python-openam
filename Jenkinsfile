node() {

    def err = null
    currentBuild.result = "SUCCESS"

    try {
        stage 'Checkout'
            checkout scm

        stage 'Install dependencies'
            sh 'pip install pep8 pep257'

        stage 'pep checks'
            sh 'pep8 openam --ignore=E501'
            sh 'pep257 openam'

        stage 'Validate on OpenAM 12'
            sh 'bash scripts/start_docker.sh 12.0.0'
            sh 'python setup.py test'

        stop_docker()

        stage 'Validate on OpenAM 13'
            sh 'bash scripts/start_docker.sh 13.0.0'
            sh 'python setup.py test'

        stop_docker()
    }

    catch (caughtError) {
        err = caughtError
        currentBuild.result = "FAILURE"
        stop_docker()
    }

    finally {
        if (err) {
            throw err
        }
    }
}

def notifyFailed() {
    emailext (
        subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
        body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
        <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
        replyTo: 'jenkins@dj-wasabi.nl',
        to: 'werner@dj-wasabi.nl',
        attachLog: true
    )
}

def stop_docker() {
    stage 'Stop container'
        sh 'bash scripts/stop_docker.sh'
}
