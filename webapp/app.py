import os
from dotenv import load_dotenv, find_dotenv
from .neo4j_connection import Neo4jConnection
from flask import Flask, g, Blueprint, render_template, request 

# load environment variables
load_dotenv(find_dotenv())

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")

main = Blueprint("main",__name__, template_folder="templates")

@main.route("/")
def home():
    return render_template("base.html")

@main.route("/similar-user")
def similar_user():
    return render_template("index.html")



@main.route("/search-book")
def search_book():
    return "<h1>Similar books</h1>"


@main.route("/search/")
def search_books():
    q = request.args.get("q")
    if q:
        db_session = get_db()
        results = db_session.get_books(uid=q)
    else:
        results = []

    return render_template("search_results.html", results=results)

def get_db():
    if not hasattr(g, 'neo4j'):
        g.neo4j = Neo4jConnection(DB_URL, DB_USERNAME, DB_PASSWORD)
    return g.neo4j

#@main.teardown_appcontext
def close_db():
    if hasattr(g, 'neo4j'):
        g.neo4j.close()



# if __name__ == "__main__":
#     app = Flask(__name__)
#     app.register_blueprint(main)
#     app.run()
