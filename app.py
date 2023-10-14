import os
import sqlite3

from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd, euro

# Configure application
app = Flask(__name__)

# Custom filter
# app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["euro"] = euro

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure the db connnection
connection = sqlite3.connect("budget.db", check_same_thread=False)
# configure a connection cursor
cur = connection.cursor()



def select_recent_expenses(user_id, number):
    answer = []

    cur.execute(
        "SELECT id, amound, type, spent_at FROM transactions WHERE user_id = ? ORDER BY spent_at DESC LIMIT ?",
        [user_id,
        number,]
    )
    names = list(map(lambda x: x[0], cur.description))
    rows = cur.fetchall()
    for row in rows:
        answer.append(dict(zip(names, row)))
    return answer


def select_sum_of_category(user_id, number):
    answer = []

    cur.execute(
        "SELECT SUM(amound) as sum, type FROM transactions WHERE user_id = ? GROUP BY type ORDER BY spent_at DESC LIMIT ?",
        [user_id,
        number,]
    )
    names = list(map(lambda x: x[0], cur.description))
    rows = cur.fetchall()
    for row in rows:
        answer.append(dict(zip(names, row)))
    return answer


def select_sum_of_category_by_date(user_id, date_str):
    answer = []
    cur.execute(
        "SELECT SUM(amound) AS sum, type FROM transactions WHERE user_id = ? AND spent_at LIKE ? GROUP BY type",
        [user_id,
        date_str + "%",]
    )
    names = list(map(lambda x: x[0], cur.description))
    rows = cur.fetchall()
    for row in rows:
        answer.append(dict(zip(names, row)))
    return answer


def select_sum_by_date(user_id, date_str):
    answer = []
    cur.execute(
        "SELECT SUM(amound) AS sum, spent_at FROM transactions WHERE user_id = ? AND spent_at LIKE ? GROUP BY spent_at",
        [user_id,
        date_str + "%",]
    )
    names = list(map(lambda x: x[0], cur.description))
    rows = cur.fetchall()
    for row in rows:
        answer.append(dict(zip(names, row)))
    return answer
    

def select_sum_by_month(user_id, date_str):
    answer = []   
    cur.execute(
        "SELECT SUM(amound) AS sum,  STRFTIME('%Y-%m', spent_at) as spent_at FROM transactions WHERE user_id = ? AND spent_at LIKE ? GROUP BY STRFTIME('%Y-%m', spent_at)",
        [user_id,
        date_str + "%",]
    )
    names = list(map(lambda x: x[0], cur.description))
    rows = cur.fetchall()
    for row in rows:
        answer.append(dict(zip(names, row)))
    return answer


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show history of todays transactions by user"""
    rows = select_recent_expenses(session["user_id"], 10)
    sums = select_sum_of_category(session["user_id"], 10)
    return render_template("home.html", rows=rows, sums=sums)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # Query database for transaction types
    cur.execute("SELECT type FROM tr_types")
    rows = cur.fetchall()
    types = []
    for row in rows:
        types.append(row[0])

    if request.method == "POST":
        # ensure a type was submited and was in registered types
        if not request.form.get("type") or request.form.get("type") not in types:
            return apology("must provide a type from the selection", 400)
        # ensure an amound was submitted
        elif not request.form.get("amound") or float(request.form.get("amound")) < 0:
            return apology("must provide a non zero number", 400)
        # ensure a date was provided
        elif not request.form.get("date"):
            return apology("must provide a valid date", 400)
        # ensure it is a valid date
        date = request.form.get("date")

        cur.execute(
            "INSERT INTO transactions (user_id, type, amound, spent_at) VALUES (?,?,?,?)",
            [session["user_id"],
            request.form.get("type"),
            round(float(request.form.get("amound")), 2),
            request.form.get("date"),]
        )
        connection.commit()

        return redirect("/")

    else:
        if len(rows) > 0:
            return render_template("add.html", rows=types)


@app.route("/home")
@login_required
def day_tracker():
    """Show history of todays transactions by user"""

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        cur.execute('SELECT * FROM users WHERE username = ?', [request.form.get("username")])
        rows = cur.fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][2], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif cur.execute(
            "SELECT username FROM users WHERE username = ?",
            request.form.get("username"),
        ):
            return apology("username is taken", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        # Ensure password and confirmation are identical
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation do not match", 400)
        cur.execute(
            "INSERT INTO users (username, hash) VALUES (?,?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )
        connection.commit()
        return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/delete", methods=["POST"])
@login_required
def sell():
    """Sell shares of stock"""
    cur.execute(
        "DELETE FROM transactions WHERE user_id = ? AND id = ?",
        [session["user_id"],
        request.form.get("id"),]
    )
    return redirect("/")


@app.route("/graphs", methods=["GET"])
@login_required
def graphs():
    return redirect("/graphs/monthly")


@app.route("/graphs/monthly", methods=["GET"])
@login_required
def graphs_monthly():
    current_month = (
        str(datetime.now().year) + "-" + ("0" + str(datetime.now().month))[-2::]
    )
    connection.commit()
    category_sums = select_sum_of_category_by_date(session["user_id"], current_month)
    sums_by_date = select_sum_by_date(session["user_id"], current_month)
    return render_template(
        "graphs.html", category_sums=category_sums, sums_by_date=sums_by_date
    )


@app.route("/graphs/yearly", methods=["GET"])
@login_required
def graphs_yearly():
    current_year = str(datetime.now().year)
    category_sums = select_sum_of_category_by_date(session["user_id"], current_year)
    sums_by_date = select_sum_by_month(session["user_id"], current_year)
    return render_template(
        "graphs.html", category_sums=category_sums, sums_by_date=sums_by_date
    )
