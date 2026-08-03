#!/bin/bash
# Check if application is running and stop it
if pgrep -f "python3 app.py" > /dev/null; then
  pkill -f "python3 app.py"
  echo "Application stopped"
else
  echo "Application was not running"
fi

# Allow time for the process to stop
sleep 5

# Force kill if still running
if pgrep -f "python3 app.py" > /dev/null; then
  pkill -9 -f "python3 app.py"
  echo "Application force stopped"
fi

# Exit with success to tell CodeDeploy deployment can continue
exit 0