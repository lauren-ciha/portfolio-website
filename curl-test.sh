#!/bin/bash

# Tests GET and POST using Bash


# create timeline post using POST
output=$(curl -s -X POST http://localhost:5000/api/timeline_post -d 'name=random&email=notanemail@gmail.com&content=Testing POST')

# check GET to make sure it was added
posts=$(curl -s http://localhost:5000/api/timeline_post)

echo "$output"
echo "$posts"

# Bonus: delete endpoint (not working at the moment, may come back to later)
# delete=$(curl -s http://localhost:5000/api/timeline_post/drandom)

# echo "$random"
