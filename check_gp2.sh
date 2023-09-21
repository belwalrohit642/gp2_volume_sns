#!/bin/bash

#gp2 nhi hota chaiye aws ---  sns  and  every ec2 instance should have 3 tags env,jira --sns and if  any available volume in aws then also mail it through sns.


ebs_volume=$(aws ec2 describe-volumes --query 'Volumes')
