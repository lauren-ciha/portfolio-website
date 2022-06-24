#!/bin/bash

# Automatically redeploys site from within the VPS. Assumes it will be run in /root

# Safety check: don't allow deployment from local machine (for now)
user="$(whoami)"
if [[ $user == *"root"* ]]; then
  echo "On SSH"
else
  echo "On local machine. Try again on SSH."
  exit 0
fi

# cd into your project folder.
cd project-shiny_sharks

# Run `git fetch && git reset origin/main --hard` to make sure the git repository inside your VPS has the latest changes from the main branch on GitHub.
git fetch && git reset origin/main --hard

# Enter the python virtual environment and Install python dependencies.
cd python3-virtualenv
python -m ensurepip --upgrade
pip3 install -r ~/project-shiny_sharks/requirements.txt

# Restarts the flask app with myportfolio.service
cd ~/project-shiny_sharks
systemctl restart myportfolio