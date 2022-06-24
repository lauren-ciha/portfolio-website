#!/bin/bash

user="$(whoami)"

# Safety check: don't allow me to redeploy site from local machine (for now)
if [[ $user == *"root"* ]]; then
  echo "On SSH"
else
  echo "On local machine. Try again on SSH."
  exit 0
fi

# Kill all existing tmux sessions. This is to kill any existing flask server that might be running in the background.
tmux kill-server

# cd into your project folder.
cd project-shiny_sharks

# Run `git fetch && git reset origin/main --hard` to make sure the git repository inside your VPS has the latest changes from the main branch on GitHub.
git fetch && git reset origin/main --hard

# Enter the python virtual environment and Install python dependencies.
cd python3-virtualenv
python -m ensurepip --upgrade
pip3 install -r ~/project-shiny_sharks/requirements.txt

# Start a new detached Tmux session that goes to the project directory, enters the python virtual environment and starts the Flask server.
cd ~/project-shiny_sharks
tmux new -d -s portfolio
tmux send-keys -t portfolio: 'source python3-virtualenv/bin/activate' 'Enter' 'export FLASK_APP=app' 'Enter' 'export FLASK_ENV=production' 'Enter' 'flask run --host=shiny-shark.duckdns.org' 'Enter'
