from webapp.service.service import Service
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)

main = Blueprint("main", __name__, template_folder="templates")


service = Service()


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
    return render_template("top-ten.html", results=service.get_top_ten())


@main.route("/insert-book", methods=["GET", "POST"])
def insert_book():
    if request.method == "POST":
        book = {
            "title": request.form["title"],
            "author": request.form["author"],
            "year": request.form["year"],
            "publisher": request.form["publisher"],
            "isbn": request.form["isbn"],
        }

        if len(book["isbn"]) != 10:
            flash("Please insert a valid isbn", "error")
            return redirect(url_for("main.insert_book"))

        result = service.insert_book(book)
        if result:
            flash("Book inserted successfully!", "success")
        else:
            flash("Something went wrong", "error")

        return redirect(url_for("main.insert_book"))
    else:
        return render_template("insert-book.html")


@main.route("/search-by-user/")
def search_books_by_user():
    q = request.args.get("q")
    if q:
        results = service.get_books_by_user(q)
    else:
        results = []
    return render_template("search-results.html", results=results)


@main.route("/search-by-book/")
def search_books_by_title():
    q = request.args.get("q")
    
    results = []
    if len(q) >= 4 and q:
        results = service.get_books_by_title(q)

    return render_template("search-results.html", results=results)

