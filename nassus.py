from flask import Flask,render_template
from store import Store
app= Flask(__name__)

@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/general-store/", defaults={'level': None})
@app.route("/general-store/<level>")
def generate_general(level):
	print(level)
	store=Store("general_store")
	if level is not None:
		store.generate_items_list(level)
	tables,titles=store.get_item_tables()
	return render_template("store.html",name="General Store",tables=[table.to_html(classes="general-table",index=False) for table in tables],titles=titles,levels=["Level 1","Level 2"])