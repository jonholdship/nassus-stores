from flask import Flask,render_template,redirect
from store import Store
app= Flask(__name__)

@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/store/<store_type>/", defaults={'level': None})
@app.route("/store/<store_type>/<level>")
def get_store_front(store_type,level):
	print(level)
	store=Store(store_type)
	if level is not None:
		store.generate_items_list(level)
		return redirect(f"/store/{store_type}/")
	tables,titles=store.get_item_tables()
	return render_template("store.html",name="General Store",tables=[table.to_html(classes="general-table",index=False) for table in tables],titles=titles,store=store.store)