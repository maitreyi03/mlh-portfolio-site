import os
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
import _osx_support
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)

print(mydb)

class TimeLinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimeLinePost])

# --- Site basics (placeholders — personalize these later) ---
NAME = "Maitreyi Pareek"
TAGLINE = "Student @ UCLA"
PHOTO = "logo.jpg"  #

# Pages shown in the dynamic navigation bar. Add a route + an entry
# here and it automatically appears in the menu.
PAGES = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Hobbies", "endpoint": "hobbies"},
    {"name": "Timeline", "endpoint": "timeline"},
]

ABOUT = (
    "Hi, I'm Maitreyi Pareek. I am currently pursuing a Masters in Applied AI, Data Science at UCLA "
    "and my background is in [xyz]. I am currently interested in [abc]."
)

EDUCATION = [
    {
        "school": "Enter University",
        "degree": "B.S. in Enter Program",
        "period": "20XX — 20XX",
    },
]

# Places I've traveled to. Each entry carries lat/lng so it can be
# plotted as a marker on the interactive Leaflet map (see index.html).
PLACES = [
    {"flag": "🇺🇸", "city": "San Francisco", "country": "USA", "lat": 37.7749, "lng": -122.4194},
    {"flag": "🇯🇵", "city": "Tokyo", "country": "Japan", "lat": 35.6762, "lng": 139.6503},
    {"flag": "🇫🇷", "city": "Paris", "country": "France", "lat": 48.8566, "lng": 2.3522},
    {"flag": "🇨🇦", "city": "Toronto", "country": "Canada", "lat": 43.6532, "lng": -79.3832},
]

HOBBIES = [
    {
        "section": "Outdoor",
        "hobbies": [
            {"name": "Hiking", "description": "Exploring trails and nature.", "icon": "🥾"},
            {"name": "Cycling", "description": "Long rides through the city and countryside.", "icon": "🚴"},
        ],
    },
    {
        "section": "Creative",
        "hobbies": [
            {"name": "Photography", "description": "Capturing moments and places.", "icon": "📷"},
            {"name": "Sketching", "description": "Drawing portraits and landscapes.", "icon": "✏️"},
        ],
    },
    {
        "section": "Tech & Gaming",
        "hobbies": [
            {"name": "Hackathons", "description": "Building projects under pressure.", "image": "vit.jpeg"},
            {"name": "Gaming", "description": "Strategy and indie games.", "icon": "🎮"},
        ],
    },
]

SKILLS = [
    {
        "group": "Languages",
        "skills": ["Language#1", "Language#2", "Language#3", "Language#4"],
    },
    {
        "group": "Frameworks",
        "skills": ["Framework#1", "Framework#2", "Framework#3", "Framework#4"],
    },
    {
        "group": "Tools",
        "skills": ["Tool#1", "Tool#2", "Tool#3", "Tool#4"],
    },
]

WORK_EXPERIENCES = [
    {
        "role": "Enter Role",
        "company": "Enter Company",
        "period": "20XX-20XX",
        "description": "Enter what you worked on.",
    },
    {
        "role": "Enter Role",
        "company": "Enter Company",
        "period": "20XX-20XX",
        "description": "Enter what you worked on."
    },
    {
        "role": "Enter Role",
        "company": "Enter Company",
        "period": "20XX-20XX",
        "description": "Enter what you worked on."
    },
]

@app.context_processor
def inject_globals():
    """Make these available to every template (powers the dynamic nav)."""
    return {
        "pages": PAGES,
        "name": NAME,
        "url": os.getenv("URL"),
        "year": datetime.now().year,
    }


@app.route("/")
def index():
    return render_template(
        "index.html",
        title=f"{NAME} · Portfolio",
        tagline=TAGLINE,
        photo=PHOTO,
        about=ABOUT,
        skills=SKILLS,
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
        places=PLACES,
    )


@app.route("/hobbies")
def hobbies():
    return render_template(
        "hobbies.html",
        title=f"Hobbies · {NAME}",
        hobbies=HOBBIES,
    )

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimeLinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimeLinePost.select().order_by(TimeLinePost.created_at.desc())
        ]
    }

@app.route("/timeline")
def timeline():
    return render_template(
        "timeline.html",
        title="Timeline",
        pages=PAGES
    )