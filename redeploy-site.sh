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

# Spin containers down to prevent out of memory issues on our VPS instances when building in the next step
docker compose -f docker-compose.prod.yml down

# Build and spin up!
docker compose -f docker-compose.prod.yml up -d --build
