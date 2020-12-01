from flask import Flask,render_template
from store import Store
app= Flask(__name__)

@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/general-store")
def general():
	store=Store("general_store.csv")
	tables,titles=store.get_item_tables()
	return render_template("store.html",tables=[table.to_html(classes="general-table",index=False) for table in tables],titles=titles)