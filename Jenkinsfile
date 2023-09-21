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
    stage('Check EC2 Instances') {
        try {
                
                def environmentTag = 'environment'
                def jiraTag = 'jira'
                
                def ec2Instances = sh(script: "aws ec2 describe-instances --query 'Reservations[].Instances[].{InstanceId:InstanceId, Tags:Tags}' --output json", returnStdout: true).trim()
                def ec2InstancesJson = readJSON(text: ec2Instances)
                
                def instancesWithTags = []
                
                ec2InstancesJson.each { instance ->
                    def tags = instance.Tags
                    def hasEnvironmentTag = false
                    def hasJiraTag = false
                    
                    tags.each { tag ->
                        if (tag.Key == environmentTag) {
                            hasEnvironmentTag = true
                        }
                        if (tag.Key == jiraTag) {
                            hasJiraTag = true
                        }
                    }
                    
                    if (hasEnvironmentTag && hasJiraTag) {
                        instancesWithTags.add(instance.InstanceId)
                    }
                }
                
                if (instancesWithTags) {
                    echo "EC2 instances with both 'environment' and 'jira' tags found: ${instancesWithTags.join(', ')}"
                } else {
                    echo "No EC2 instances found with both 'environment' and 'jira' tags."
                }
            
        } catch (Exception e) {
            error "Error checking EC2 instances: ${e.message}"
        }
    }
}




