import pandas as pd
from os.path import join
import numpy as np
import json

DATA_FOLDER="static/data"

json_files={
	"general_store":join(DATA_FOLDER,"jsons/","general_store.json"),
	"blacksmith":join(DATA_FOLDER,"jsons/","blacksmith.json")
}

item_files={
	"general_store":join(DATA_FOLDER,"general_store_items.csv"),
	"blacksmith":join(DATA_FOLDER,"blacksmith_items.csv")

}


class Store:
	'''
	Class to handle the item filtering and randomization logic.
	Probability of an item appearing in the store and mark ups are stored in a csv file which is loaded
	Beyond that, the logic is generic so we should manage with a single store class
	'''
	def __init__(self,store_type,level=1):
		'''
		initialize a specific store by providing the store specific probability file and upgrade level
		'''
		with open(json_files[store_type],"r") as f:
			self.store=json.load(f)
			self.level=self.store["level"]

		self.rule_file=join(DATA_FOLDER,"rules/",self.store["levels"][self.level])
		self.item_file=item_files[store_type]
		self.current_level=level
		
	def get_item_tables(self):
		'''
		Function returns two lists: 
		table - a list with one pandas dataframe per item type/subtype combo
		titles - names of tables
		The content of these tables is set by self.get_items()
		'''
		table=pd.read_csv(self.item_file)
		table["Title"]=table["Type"]+" ("+table["Subtype"]+")"
		titles=table["Title"].unique()
		table=[table[table["Title"]==x].drop("Title",axis=1).fillna("-") for x in titles]
		return table,titles

	def generate_items_list(self,level):
		'''
		Function that uses the information in the store specific file to filter the item lists
		Calls a random number generator to determine whether items are in stock
		Applies mark up
		'''
		#load items and filter table 
		print(self.rule_file)
		rule_df=pd.read_csv(self.rule_file)
		print(rule_df)
		rule_df=rule_df[rule_df["Level"]==self.current_level]
		items_df=pd.read_csv(join(DATA_FOLDER,"mundane.csv")).merge(rule_df,on=["Type","Subtype"],how="inner")

		#get a random number for every row (0-1) and keep if lower than probability of item being in stock
		idx=items_df["probability"].map(lambda x: np.random.uniform()<x)

		#sort by type,subtype and name for alphabetised lists
		items_df=items_df.loc[idx].drop(["probability","Level"],axis=1).sort_values(["Type","Subtype","Name"])

		#mark up
		items_df["Price"]=items_df["Value"].astype(float)*items_df["mark_up"].astype(float)
		items_df["Price"]=items_df["Value"].fillna(999).astype(int).astype(str)+" "+items_df["Unit"]
		items_df=items_df.drop(["Value","Unit","mark_up"],axis=1)
		items_df.to_csv(self.item_file,index=False)