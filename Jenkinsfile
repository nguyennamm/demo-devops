pipeline {
    agent none
    environment {
        ENV = 'dev'
        NODE = 'Build-server-demo'
    }

    stages {
        stage('Build Image') {
            agent {
                node {
                    label "$NODE"
                }
            }
            environment {
                TAG = sh(returnStdout: true, script: 'git rev-parse -short=10 HEAD | tail -n +2').trim()
                DOCKER_HUB_CREDS = credentials('jenkins-dockerhub-common-creds')
                MYSQL_CREDS = credentials('jenkins-mysql-demo-devops-creds')
            }
            steps {
                sh """
                    docker build nodejs/. -t demo-devops-nodejs-$ENV:latest \
                    --build-arg MYSQL_USER=$MYSQL_CREDS_USR \
                    --build-arg MYSQL_PWD=$MYSQL_CREDS_PSW \
                    -f nodejs/Dockerfile
                    """
                sh "docker login -u $DOCKER_HUB_CREDS_USR -p $DOCKER_HUB_CREDS_PSW"
                // tag docker image
                sh "docker tag demo-devops-nodejs-$ENV:latest namnguyen96/demo-devops:$TAG"
                //push docker image to docker hub
                sh "docker push namnguyen96/demo-devops:$TAG"
                // remove docker image to reduce space on build server
                sh "docker rmi -f namnguyen96/demo-devops:$TAG"
            }
        }
        stage('Deploy') {
            agent {
                node {
                    label 'Target-server-demo'
                }
            }
            environment {
                TAG = sh(returnStdout: true, script: 'git rev-parse -short=10 HEAD | tail -n +2').trim()
                MYSQL_CREDS = credentials('jenkins-mysql-demo-devops-creds')
            }
            steps {
                sh """
                    docker-compose build \
                    --build-arg TAG=$TAG \
                    --build-arg MYSQL_USER=$MYSQL_CREDS_USR \
                    --build-arg MYSQL_PWD=$MYSQL_CREDS_PSW
                    """
                sh 'docker-compose up -d'
            }
        }
    }
}
