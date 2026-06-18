import os
from datetime import datetime

from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- Site basics (placeholders — personalize these later) ---
NAME = "Thomas"
TAGLINE = "MLH Fellow/Software Engineer"
PHOTO = "logo.jpg"  # 

# Pages shown in the dynamic navigation bar. Add a route + an entry
# here and it automatically appears in the menu.
PAGES = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Hobbies", "endpoint": "hobbies"},
]

ABOUT = (
    "Hi, I'm Thomas, I love building useful things on the web! "
    "I'm super excited to be a part of the MLH Fellowship! "
    "I have a passion for software engineering and I'm always looking for new challenges and opportunities to grow."
)

EDUCATION = [
    {
        "school": "University of Waterloo",
        "degree": "B.S. in Mathematics",
        "period": "2025 — 2030",
    },
]

# Simple list-style "travel map" for now — we'll upgrade to an
# interactive map later.
PLACES = [
    {"flag": "🇺🇸", "city": "San Francisco", "country": "USA"},
    {"flag": "🇯🇵", "city": "Tokyo", "country": "Japan"},
    {"flag": "🇫🇷", "city": "Paris", "country": "France"},
    {"flag": "🇨🇦", "city": "Toronto", "country": "Canada"},
]

HOBBIES = [
    {
        "name": "Hackathons",
        "description": "I love hackathons."
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
