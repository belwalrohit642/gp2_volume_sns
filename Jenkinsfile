node {
    def SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:640284417783:gp2_volume'

    try {
        stage('Check EBS Volumes') {
            def ebs_volumes = sh(script: 'aws ec2 describe-volumes --query \'Volumes\'', returnStdout: true).trim()

            if (ebs_volumes.contains("\"VolumeType\": \"gp2\"")) {
                echo "There are gp2 EBS volumes in your AWS account."

                // sh "aws sns publish --topic-arn $SNS_TOPIC_ARN --subject 'GP2 EBS Volumes Found' --message 'There are gp2 EBS volumes in your AWS account.'"
            } else {
                echo "No gp2 EBS volumes found in your AWS account."
            }
        }
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        error("Check EBS Volumes stage failed: ${e.message}")
    }
    try {
        stage('Check EC2 Instances') {
            def awsRegion = 'us-east-1' 
            def environmentTag = 'environment'
            def jiraTag = 'jira'
            def snsTopicArn =  'arn:aws:sns:us-east-1:640284417783:gp2_volume'

            def describeInstancesCmd = """
                aws ec2 describe-instances \
                --region $awsRegion \
                --filters "Name=tag:environment,Values=$environmentTag" "Name=tag:jira,Values=$jiraTag" \
                --query "Reservations[].Instances[].InstanceId" \
                --output text
            """

               def instances = sh(script: describeInstancesCmd, returnStatus: true, returnStdout: true).trim()

            if (instances) {
                echo "Found EC2 instances with both 'environment' and 'jira' tags."

                def publishSnsCmd = """
                    aws sns publish \
                    --region $awsRegion \
                    --topic-arn $snsTopicArn \
                    --message "EC2 instances with both 'environment' and 'jira' tags were found."
                """

                sh(script: publishSnsCmd)
            } else {
                echo "No EC2 instances found with both 'environment' and 'jira' tags."
            }
        }

        stage('Check EBS Volumes') {
            def describeVolumesCmd = """
                aws ec2 describe-volumes \
                --region $awsRegion \
                --query "Volumes"
            """

            def volumes = sh(script: describeVolumesCmd, returnStatus: true).trim()

            if (volumes) {
                echo "There are EBS volumes in your AWS account."
            } else {
                echo "No EBS volumes found in your AWS account."
            }
        }
    } catch (Exception e) {
        echo "Error: ${e.message}"
        currentBuild.result = 'FAILURE'
        error("Pipeline failed")
    }

}
