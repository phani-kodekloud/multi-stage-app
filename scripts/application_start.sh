#!/bin/bash
# Navigate to app directory
cd /home/ec2-user/app

# Kill any existing process if running on port 80
sudo fuser -k 80/tcp || true

# Start the application with nohup
nohup python3 app.py > app.log 2>&1 &

# Exit with success to tell CodeDeploy deployment succeeded
exit 0