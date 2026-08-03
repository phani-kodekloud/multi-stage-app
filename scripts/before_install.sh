
#!/bin/bash
# Create application directory if it doesn't exist
if [ ! -d /home/ec2-user/app ]; then
  mkdir -p /home/ec2-user/app
fi

# Skip pip upgrade to avoid RPM conflicts on Amazon Linux 2023
echo "✅ Skipping pip upgrade to avoid RPM conflicts"
echo "Current pip version:"
pip3 --version