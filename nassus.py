from flask import Flask,render_template,redirect
from store import Store
from pandas import read_csv
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

@app.route("/council/")
def get_rumors():
	sheet="https://docs.google.com/spreadsheets/d/1010E504bSwUuVMSt1v-OGkZYjq2V95Xn0cYXXtbNTi0/"
	rumours=read_csv(f"{sheet}export?gid=0&format=csv")
	return render_template("council.html",name="Rumours",rumours=rumours,sheet=sheet)