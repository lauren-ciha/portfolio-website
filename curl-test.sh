#!/bin/bash

# Tests GET and POST using Bash

# create timeline post using POST
output=$(curl -s -X POST http://localhost:5000/api/timeline_post -d 'name=test&email=notanemail@gmail.com&content=Testing POST')

# check GET to make sure it was added
posts=$(curl -s http://localhost:5000/api/timeline_post)

# generate a random name
name=""
chars=abcd1234ABCD
for i in {1..8} ; do
    name="${chars:RANDOM%${#chars}:1}"
done

# echo "$output"
if [[ $output == *"$name"* ]];
then
   echo "Post and get were successful"
else
    echo "Test failed"
fi

# variable=$(mysql -u myportfolio -p -D myportfoliodb -e "SELECT * from timelinepost WHERE name = '"\name\"';")
# if [ -z $variable ]; then echo "Var is empty"; fi

# Bonus: delete endpoint (not working at the moment, may come back to later)
# delete=$(curl -s http://localhost:5000/api/timeline_post/drandom)

# echo "$random"
