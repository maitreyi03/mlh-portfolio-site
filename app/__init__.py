import os
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
import _osx_support
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

# Use an in-memory SQLite DB when running tests (TESTING=true) so the test
# suite never touches the real MySQL. Otherwise connect to MySQL as usual.
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )

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
    "Hi, I'm Maitreyi Pareek, currently pursing a Master of Engineering in Applied AI at UCLA "
    "I graudted with a B.S. in Computer Science & Engineering graduate from UCIrvine last year"
    "I am currenly participating as a Production Engineering Fellow with the Meta & MLH Fellowship"
    "and completing my Capstone Project as a Data Analyst with Takeda- a BioPharm company in LA"
    "and working on the plasma fractionation process"
)

EDUCATION = [
    {
        "school": "University of California, Los Angeles (UCLA)",
        "degree": "M.Eng., Data Science, Applied Machine Learning",
        "period": "Sep 2025 — Aug 2026",
    },
    {
        "school": "University of California, Irvine (UCI)",
        "degree": "B.S., Computer Science & Engineering",
        "period": "Sep 2021 — Jun 2025",
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
        "skills": ["Python", "Java", "C++", "React", "SQL"],
    },
    {
        "group": "Systems & Backend",
        "skills": [
            "Databases", "OS", "Distributed Systems", "Multithreading",
            "Concurrency", "Linux", "Docker", "CI/CD",
        ],
    },
    {
        "group": "Cloud & Tooling",
        "skills": ["AWS", "GCP", "Git"],
    },
]

PROJECTS = [
    {
        "letter": "A",
        "title": "Reflective Hybrid RAG for Recommendations",
        "kicker": "Agentic AI Project",
        "description": (
            "Improved top-1 recommendation accuracy 3× (12.5% → 37.5% HR@1) with a reflective "
            "hybrid RAG system separating raw user history from synthesized preference memory. "
            "Lifted personalization quality across ranking metrics (+25% HR@10) by combining dense "
            "embeddings and sparse SPLADE retrieval with LLM-generated user personas."
        ),
        "tags": ["RAG", "LLM Agents", "SPLADE", "Recommender Systems"],
        "github": "https://github.com/maitreyi03/AgentSocietyChallenge",
        "has_paper": True,
    },
    {
        "letter": "B",
        "title": "Adaptive Subset Selection for Federated Learning",
        "kicker": "FedAvg, FedProx",
        "description": (
            "Cut federated training cost 70% per client via adaptive coreset selection while "
            "preserving accuracy under FedAvg on non-IID CIFAR-100 partitions. Built a reproducible "
            "federated evaluation framework across 20 training rounds using ResNet-18 with "
            "client-side subset selection under realistic non-IID constraints."
        ),
        "tags": ["Federated Learning", "ResNet-18", "CIFAR-100", "Adaptive Coreset Selection"],
        "github": "https://github.com/maitreyi03/fed-craig",
        "has_paper": True,
    },
    {
        "letter": "C",
        "title": "Virtual File System",
        "kicker": "Systems Programming",
        "description": (
            "Engineered a virtual file system in Java with an I/O subsystem, open file table, "
            "bitmap-based block allocation, and file descriptors, enabling directory management, "
            "metadata tracking, and efficient block-level file access."
        ),
        "tags": ["Java", "Operating Systems", "File Systems"],
        "github": "https://github.com/maitreyi03/Virtual-File-System/",
        "has_paper": False,
    },
    {
        "letter": "D",
        "title": "Search Engine, Information Retrieval System",
        "kicker": "Information Retrieval",
        "description": (
            "Built a Python search engine over 37,000 documents using a custom inverted index and "
            "TF-IDF ranking, improving retrieval with stemming, term weighting, duplicate detection, "
            "and multi-term query support."
        ),
        "tags": ["Python", "TF-IDF", "Inverted Index", "IR"],
        "github": "https://github.com/ijena/search-engine",
        "has_paper": False,
    },
]

WORK_EXPERIENCES = [
    {
        "role": "Production Engineering Fellow",
        "company": "Meta & MLH Fellowship",
        "period": "Jun 2026 – Aug 2026",
        "description": (
            "Working with Meta engineers on production engineering projects focused on "
            "reliability and scalable infrastructure."
        ),
    },
    {
        "role": "Data Analyst Intern",
        "company": "Takeda",
        "period": "Jun 2026 – Aug 2026",
        "description": (
            "Building AI/ML models for Takeda's plasma fractionation, leveraging PAT, "
            "Databricks, SIMCA Online, and image processing to improve monitoring, "
            "deviation detection, and process optimization."
        ),
    },
    {
        "role": "Web Application QA Engineer",
        "company": "UCI Office of Information and Technologies",
        "period": "Apr 2023 – Jun 2025",
        "description": (
            "Created and conducted comprehensive exploratory and regression test plans "
            "across 9 Canvas instructor tools, using Selenium and Postman to validate UI "
            "workflows and API behavior, reporting 150+ bugs via Jira. Deployed branches on "
            "Jenkins and simulated user interactions to uncover system-wide bugs and correlations."
        ),
    },
    {
        "role": "Research Assistant with Professor QV",
        "company": "ZotPonics Lab, UC Irvine",
        "period": "Jan 2024 – Feb 2025",
        "description": (
            "Built an IoT pipeline to transmit live pH, nutrient, and moisture sensor data "
            "into MySQL through a Flask REST API and React Native dashboard. Trained and "
            "deployed a CNN to detect plant health issues (nutrient deficiency, pH imbalance) "
            "from leaf images."
        ),
    },
    {
        "role": "Software Engineering Intern",
        "company": "BRDG Research – Internship",
        "period": "Jun 2024 – Sep 2024",
        "description": (
            "Developed an end-to-end PVC repurposing solution — a full-stack donation intake "
            "application built with Python, Flask, and MySQL that let users upload images and "
            "receive classification feedback. Integrated a fine-tuned MobileNetV2 image "
            "classifier using transfer learning to identify PVC-containing items, and "
            "authored two first-authored technical papers on the AI-enhanced recycling system."
        ),
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
        projects=PROJECTS,
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
    name = request.form.get("name")
    email = request.form.get("email")
    content = request.form.get("content")

    # Validate input before writing to the database (return 400 on bad input).
    if not name:
        return "Invalid name", 400
    if not content:
        return "Invalid content", 400
    if not email or "@" not in email:
        return "Invalid email", 400

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