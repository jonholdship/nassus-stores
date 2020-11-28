from flask import Flask,render_template
from pandas import read_csv
app= Flask(__name__)

@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/general-store")
def general():
	mundane=read_csv("static/item-data/mundane.csv")
	return render_template("store.html",tables=[mundane.to_html(classes="general-table",index=False)],titles=["mundane"])