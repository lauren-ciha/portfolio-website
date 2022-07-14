from email.policy import default
import os
from select import select
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv('TESTING') == 'true':
    print('Running in test mode')
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:    
    mydb=MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
    )

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database=mydb

mydb.connect()
mydb.create_tables([TimelinePost])

lauren_info = {"name":"Lauren Ciha",
"university":"University of Wisconsin",
"degree":"BA, Computer Science and Philosophy",
"years":"2019-2023",
"github":"https://github.com/lauren-ciha",
"linkedin": "https://linkedin.com/in/lauren-ciha",
"calendly":"https://calendly.com/lauren-ciha",
"activities":"",
"skills":"",
"about":""}

#Lauren
laurenExperience = ["Schloss Visual Reasoning Lab", "People and Robots Lab", "MLH Fellowship"]
laurenHobbies = ["Reading", "Journaling", "Running"]

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('lauren.html', 
    title=lauren_info["name"],
    university=lauren_info["university"],
    years=lauren_info["years"],
    degree=lauren_info["degree"],
    experience_list=laurenExperience,
    hobby_list = laurenHobbies,
    url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", timeline=get_time_line_post())

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    
    # Running error handling to make sure the user input is correct data -Malik

    test_name = request.form.get('name')
    if test_name is None or test_name == "":
        return "Invalid name", 400
    else:
        name = request.form['name']

    test_email =  request.form.get('email')
    if "@" not in test_email or test_email is None:
        return "Invalid email", 400
    else:
        email = request.form['email']

    test_content = request.form.get('content')
    if test_content == "" or test_content is None:
        return "Invalid content", 400
    else:
        content =  request.form['content']       
    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [ 
            model_to_dict(p)
            for p in 
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
    }

@app.route('/test', methods=['POST'])
def post_time_line_post_test():
    # Running error handling to make sure the user input is correct data -Malik

    name = request.form['name']    
    
    timeline_post = TimelinePost.create(name=name, email="email@email.com", content="content")
    return model_to_dict(timeline_post)

if __name__ == '__main__':
    app.run(debug=True)