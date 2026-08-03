#!/bin/bash
# Navigate to app directory
cd /home/ec2-user/app

# Install required dependencies
pip3 install -r requirements.txt

# Set environment variable based on EC2 tags
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | sed 's/[a-z]$//')
ENVIRONMENT=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=Environment" --region $REGION --query "Tags[0].Value" --output text)

# Update the environment in app.py
sed -i "s/ENVIRONMENT_PLACEHOLDER/$ENVIRONMENT/g" /home/ec2-user/app/app.py