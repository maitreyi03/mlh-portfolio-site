import os
from datetime import datetime

from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- Site basics (placeholders — personalize these later) ---
NAME = "Thomas"
TAGLINE = "MLH Fellow · Software Engineer"
PHOTO = "logo.jpg"  # replace with a real photo in app/static/img/

# Pages shown in the dynamic navigation bar. Add a route + an entry
# here and it automatically appears in the menu.
PAGES = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Hobbies", "endpoint": "hobbies"},
]

ABOUT = (
    "Hi, I'm Thomas — a software engineer and MLH Fellow who likes building "
    "useful things on the web. This portfolio is the starting point I'll keep "
    "improving throughout the fellowship."
)

EXPERIENCES = [
    {
        "role": "Software Engineer",
        "company": "Viggle",
        "period": "2024 — Present",
        "description": "Building product features and shipping to users.",
    },
    {
        "role": "Software Engineering Intern",
        "company": "Previous Company",
        "period": "2023",
        "description": "Worked across the stack on internal tooling.",
    },
]

EDUCATION = [
    {
        "school": "Your University",
        "degree": "B.S. in Computer Science",
        "period": "2021 — 2025",
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
        "name": "Photography",
        "description": "Capturing cities and landscapes on weekends.",
        "image": "https://picsum.photos/seed/photography/600/400",
    },
    {
        "name": "Hiking",
        "description": "Getting outdoors and exploring new trails.",
        "image": "https://picsum.photos/seed/hiking/600/400",
    },
    {
        "name": "Coffee",
        "description": "Trying new beans and pour-over methods.",
        "image": "https://picsum.photos/seed/coffee/600/400",
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
        experiences=EXPERIENCES,
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
