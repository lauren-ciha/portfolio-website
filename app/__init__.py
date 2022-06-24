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

name = "Name"
experience_list = ["Experience 1", "Experience 2", "Experience 3"]
education_list = ["Education 1"]
hobby_list = ["Hobby 1", "Hobby 2", "Hobby 3", "Hobby 4"]

# Example for one person
# name = "Lauren Ciha"
# experience_list = ["Schloss Visual Reasoning Lab", "People and Robots Lab", "MLH Fellowship!"]
# education_list = ["University of Wisconsin-Madison"]
# hobby_list = ["reading", "journaling", "running"]

#Lauren
laurenExperience = ["Schloss Visual Reasoning Lab", "People and Robots Lab", "MLH Fellowship"]
laurenEducation = ["University of Wisconson-Madison"]
laurenHobbies = ["reading", "journaling", "running"]

#Ruchika
ruchikaExperience =["Fellow", "MLH Production Engineering Fellowship","Undergraduate Research Assistant,IUC","Math Tutor, Juni Learning"]
ruchikaEducation = ["University of Illinois at Urbana Champaign"]
ruchikaHobbies = ["drumming", "embroidery", "video games"]

#Sasha
sashaExperience = ["Fellow, MLH PE Fellowship", "Video Editor, McMaster Silhouette", "Make-Up Artist, Sephora"]
sashaEducation = ["McMaster University", "OCAD U"]
sashaHobbies = ["Photography", "Games", "Reading"]

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('homePage.html', title="Index Page", url=os.getenv("URL"))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('homePage.html', title="Index Page", url=os.getenv("URL"))

@app.route('/sasha', methods=['GET', 'POST'])
def sasha():
    return render_template('sasha.html', title="Sasha Page", experience_list=sashaExperience, education_list=sashaEducation, hobby_list = sashaHobbies,url=os.getenv("URL"))

@app.route('/lauren', methods= ['POST', 'GET'])
def lauren():
    return render_template('lauren.html', title="Lauren",experience_list=laurenExperience, education_list=laurenEducation, hobby_list = laurenHobbies, url=os.getenv("URL"))

@app.route('/ruchika', methods= ['POST', 'GET'])
def ruchika():
    return render_template('ruchika.html', title="Ruchika Page", experience_list=ruchikaExperience, education_list=ruchikaEducation, hobby_list = ruchikaHobbies, url=os.getenv("URL"))

@app.route('/sample')
def template_test():
    return render_template('sample_page.html', name = name, experience_list=experience_list, education_list=education_list, hobby_list = hobby_list, url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", timeline=get_time_line_post())

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
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

if __name__ == '__main__':
    app.run(debug=True)