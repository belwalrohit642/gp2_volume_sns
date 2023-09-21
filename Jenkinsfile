node {
    def AWS_DEFAULT_REGION = 'us-east-1'
    def SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:640284417783:gp2_volume'

    stage('Check EBS Volumes') {


        try {
            withCredentials([string(credentialsId: 'your-aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'), string(credentialsId: 'your-aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')]) {
                sh "aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID"
                sh "aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY"
                sh "aws configure set default.region $AWS_DEFAULT_REGION"

                def ebs_volumes = sh(script: 'aws ec2 describe-volumes --query \'Volumes\'', returnStdout: true).trim()

                if (ebs_volumes.contains("\"VolumeType\": \"gp2\"")) {
                    echo "There are gp2 EBS volumes in your AWS account."

                    sh "aws sns publish --topic-arn $SNS_TOPIC_ARN --subject 'GP2 EBS Volumes Found' --message 'There are gp2 EBS volumes in your AWS account.'"
                } else {
                    echo "No gp2 EBS volumes found in your AWS account."
                }
            }
        } catch (Exception e) {
            currentBuild.result = 'FAILURE'
            throw e
        }
    }
}

