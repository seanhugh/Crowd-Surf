from flask import Flask, flash, redirect, render_template, request, session, url_for
app = Flask(__name__)

@app.route("/")
def hello():
     return render_template("index.html")

if __name__ == "__main__":
    app.run()