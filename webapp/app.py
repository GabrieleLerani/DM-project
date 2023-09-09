import os
from dotenv import load_dotenv, find_dotenv
from .neo4j_connection import Neo4jConnection
from flask import Flask, g, Blueprint, render_template, request

# load environment variables
load_dotenv(find_dotenv())

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")

main = Blueprint("main", __name__, template_folder="templates")


@main.route("/")
def home():
    return render_template("base.html")


@main.route("/similar-user")
def similar_user():
    return render_template("search-user-similarities.html")


@main.route("/search-book")
def search_book():
    return render_template("search-book.html")


@main.route("/top-ten")
def search_top_ten():
    db_session = get_db()
    results = db_session.get_top_ten()

    return render_template("top-ten.html", results=results)


@main.route("/search-by-user/")
def search_books_by_user():
    q = request.args.get("q")

    if q:
        db_session = get_db()
        results = db_session.get_books(uid=q)
    else:
        results = []

    return render_template("search-results.html", results=results)


@main.route("/search-by-book/")
def search_books_by_title():
    q = request.args.get("q")
    if q:
        db_session = get_db()
        results = db_session.get_books(title=q)
    else:
        results = []

    return render_template("search-results.html", results=results)


def get_db():
    if not hasattr(g, "neo4j"):
        g.neo4j = Neo4jConnection(DB_URL, DB_USERNAME, DB_PASSWORD)
    return g.neo4j
