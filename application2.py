# THIS IS THE APPLICATION
from cs50sql import SQL as SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
import datetime

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///tickets.db")

@app.route("/")
def index():
    # Create variable to keep track of total cash and avaliable cash
    # send information for index.html to index.html
    return render_template("index.html", total=usd(total))

@app.route("/buy", methods=["GET", "POST"])
def buy():
    """Buy shares of stock."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Error Catching. Checking for lack of input / proper input
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        if not request.form.get("shares"):
            return apology("must provide shares")
        if not request.form.get("shares").isdigit():
            return apology("must provide shares")
            
        # Checks for SQL injection
        if not checkSQL(request.form.get("shares")) or not checkSQL(request.form.get("symbol")):
            return apology("Input Denied")
        
        # Gets input from user
        symbol=request.form.get("symbol")
        
        # look too see if user owns any of this stock
        stocks = db.execute("SELECT * FROM portfolio WHERE id = :id AND symbol LIKE :symbol", id=session["user_id"], symbol=symbol)
        
        # Error catching for invalid symbol
        stock_dict = lookup(symbol)
        if not stock_dict:
            return apology("invalid symbol")
        
        # Check to make sure sufficient funds
        cost = int(request.form.get("shares")) * stock_dict["price"]
        cash_left = user_cash() - cost
        if (cash_left<=0):
            return apology("insufficient funds")
        
        # Update remaining funds
        db.execute("UPDATE users SET cash = :cash WHERE ID = :id", cash = cash_left, id = session["user_id"])
        
        # If stock not yet in portfolio add to portfolio and buy
        if len(stocks) < 1:
            db.execute("INSERT INTO portfolio (id,symbol,shares) VALUES (:id,:symbol,:shares)", id=session["user_id"], symbol=symbol, shares=request.form.get("shares"))
            
        # Else if it is update the total # of stocks in portfolio
        else:
            row_id = db.execute("SELECT rowid, * FROM portfolio WHERE id LIKE :id AND symbol LIKE :symbol", id=session["user_id"], symbol=symbol)
            total_shares = int(request.form.get("shares")) + row_id[0]['shares']
            db.execute("UPDATE portfolio SET id=:id, symbol=:symbol, shares=:shares WHERE rowid = :row_id", id=session["user_id"], symbol=symbol, shares=total_shares,row_id=row_id[0]['rowid'])
        
        # Put transaction into history logs
        log_history(symbol, int(request.form.get("shares")), usd(stock_dict["price"]))
        
        # redirect user to index and alert of buy
        flash('Bought!')
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

@app.route("/history")
def history():
    """Show history of transactions."""
    # Get all data and send to the jinja page
    user_data = db.execute("SELECT * FROM history WHERE id = :id", id=session["user_id"])
    return render_template("history.html", data = user_data)
    
@app.route("/addfunds", methods=["GET", "POST"])
def addfunds():
    """Add funds to the user's account."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Error Catching. Checking for lack of input / proper input
        if not request.form.get("funds"):
            return apology("must provide quantity")
            
        # Checks for SQL injection
        if not checkSQL(request.form.get("funds")):
            return apology("Input Denied")
            
        # Makes sure a positive number is given
        if (int(request.form.get("funds")) <= 0):
            return apology("Funds must be greater than 0")
            
        # Calculates total avaliable cash
        total = user_cash() + int(request.form.get("funds"))
        
        # Returns a summary statement to user
        statement = usd(int(request.form.get("funds"))) + " has been added to your account. Your current total is now " + usd(total)
        
        # Updates cash total in user's account (db)
        db.execute("UPDATE users SET cash = :cash WHERE ID = :id", cash = total, id = session["user_id"])
        
                # Updates the page to the statement page
        return render_template("fundsadded.html", statement = statement)
        
    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("addfunds.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        if not checkSQL(request.form.get("username")):
            return apology("Input Denied")
        if not checkSQL(request.form.get("password")):
            return apology("Input Denied")
        
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
def quote():
    """Get stock quote."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")
            
        # Checks for SQL injection
        if not checkSQL(request.form.get("symbol")):
            return apology("Input Denied")
            
        # query database for symbol
        symbol=request.form.get("symbol")
        stock_dict = lookup(symbol)
        
        #error catching for invalid symbol
        if not stock_dict:
            return apology("invalid symbol")
        
        # Creates statement to show user
        statement = "A share of " + stock_dict["name"] + ", Inc. (" + stock_dict["symbol"] + ") costs " + usd(stock_dict["price"]) + "."
        
        # redirect user to the quote stament page quoted.html
        return render_template("quoted.html", statement = statement)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure both passwords are submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        elif not request.form.get("password2"):
            return apology("must provide password")
        
        # Checks for SQL injection
        if not checkSQL(request.form.get("username")):
            return apology("Input Denied")
        if not checkSQL(request.form.get("password")):
            return apology("Input Denied")
        if not checkSQL(request.form.get("password2")):
            return apology("Input Denied")
        
        # Checks to make sure passwords match
        elif (request.form.get("password") != request.form.get("password2")):
            return apology("passwords do not match")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 0:
            return apology("This username is taken")

        #Insert the user into the database
        hashed = pwd_context.encrypt(request.form.get("password"))
        db.execute("INSERT INTO users (id,username,hash) VALUES (NULL,:username,:hash)", username=request.form.get("username"), hash=hashed)

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
def sell():
    """Sell shares of stock."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Error Catching. Checking for lack of input / proper input
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        if not request.form.get("shares"):
            return apology("must provide shares")
        if not request.form.get("shares").isdigit():
            return apology("must provide shares")
            
        # checks for SQL injections
        if not checkSQL(request.form.get("shares")) or not checkSQL(request.form.get("symbol")):
            return apology("Input Denied")
            
        #set symbol variable
        symbol=request.form.get("symbol")
        
        # look too see if user owns any of this stock
        stocks = db.execute("SELECT * FROM portfolio WHERE id = :id AND symbol LIKE :symbol", id=session["user_id"], symbol=symbol)
        
        # Error catching for invalid symbol
        stock_dict = lookup(symbol)
        if not stock_dict:
            return apology("invalid symbol")
        
        # If stock not in portfolio return error
        if len(stocks) < 1:
            return apology("Stock not in portfolio")

        # Else if it is check to make sure # in portfolio >= to # that can be sold
        else:
            raw_data = db.execute("SELECT * FROM portfolio WHERE id LIKE :id AND symbol LIKE :symbol", id=session["user_id"], symbol=symbol)
            cost = int(request.form.get("shares")) * stock_dict["price"]
            user_data = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
            cash_left = user_data[0]['cash'] + cost
        
        # Check to see if the number of stocks to sell is <= to stocks owned
        if (int(request.form.get("shares")) > int(raw_data[0]['shares'])):
            return apology("Not enough Shares")
        
        # Update remaining funds
        db.execute("UPDATE users SET cash = :cash WHERE ID = :id", cash = cash_left, id = session["user_id"])
        
        # Update number of stocks in portfolio
        new_shares = (int(raw_data[0]['shares']) - int(request.form.get("shares")))
        if ( new_shares == 0):
            db.execute("DELETE FROM portfolio WHERE id LIKE :id AND symbol LIKE :symbol", id=session["user_id"], symbol=symbol)
        else:
            db.execute("UPDATE portfolio SET shares=:shares WHERE id = :id AND symbol=:symbol", shares=new_shares, id=session["user_id"], symbol=symbol)
        
        # Put transaction into history logs
        log_history(symbol, -int(request.form.get("shares")), usd(stock_dict["price"]))
        
        # redirect user to home page and alert user of sell
        flash('Sold!')
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html")

if __name__ == "__main__":
    app.run()