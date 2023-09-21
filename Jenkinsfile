node {
    def SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:640284417783:gp2_volume'

    stage('Check EBS Volumes') {
        try {
            def ebs_volumes = sh(script: 'aws ec2 describe-volumes --query \'Volumes\'', returnStdout: true).trim()
                   
            if (ebs_volumes.contains("\"VolumeType\": \"gp2\"")) {
                echo "There are gp2 EBS volumes in your AWS account."

                sh "aws sns publish --topic-arn $SNS_TOPIC_ARN --subject 'GP2 EBS Volumes Found' --message 'There are gp2 EBS volumes in your AWS account.'"
            } else {
                echo "No gp2 EBS volumes found in your AWS account."
            }
        } catch (Exception e) {
            currentBuild.result = 'FAILURE'
            throw e
        }
    }
   
    
    stage('Check EC2 Tags') {
        try {
            def ec2_instances = sh(script: 'aws ec2 describe-instances --query "Reservations[*].Instances[*]"', returnStdout: true).trim()
       
            def instances = readJSON(text: ec2_instances)
            
            def instancesWithTags = []
            
            instances.each { instance ->
                def tags = instance.Tags
                if (tags) {
                    def environmentTag = tags.find { it.Key == 'environment' }
                    def jiraTag = tags.find { it.Key == 'jira' }
                    
                    if (environmentTag && jiraTag) {
                        instancesWithTags.add(instance.InstanceId)
                    }
                }
            }
            
            if (instancesWithTags) {
                echo "Instances with both 'environment' and 'jira' tags found: ${instancesWithTags.join(', ')}"
                
                sh "aws sns publish --topic-arn $SNS_TOPIC_ARN --subject 'EC2 Instances with Tags Found' --message 'Instances with both ''environment'' and ''jira'' tags found: ${instancesWithTags.join(', ')}'"
            } else {
                echo "No instances with both 'environment' and 'jira' tags found."
            }
        } catch (Exception e) {
            currentBuild.result = 'FAILURE'
            throw e
        }
    
 
}

}
