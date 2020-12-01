import pandas as pd
from os.path import join
import numpy as np
data_folder="static/item-data"


class Store:
	def __init__(self,store_file,level=1):
		self.store_file=store_file
		self.current_level=level
		
	def get_item_tables(self):
		table=self.get_items()
		table["Price"]=table["Value"].astype(float)*table["mark_up"].astype(float)
		table["Price"]=table["Value"].fillna(999).astype(int).astype(str)+" "+table["Unit"]
		table=table.drop(["Value","Unit","mark_up"],axis=1)
		table["Title"]=table["Type"]+" ("+table["Subtype"]+")"
		titles=table["Title"].unique()
		table=[table[table["Title"]==x] for x in titles]
		return table,titles

	def get_items(self):
		store_df=pd.read_csv(join(data_folder,self.store_file))
		store_df=store_df[store_df["Level"]==self.current_level]
		items_df=pd.read_csv(join(data_folder,"mundane.csv")).merge(store_df,on=["Type","Subtype"])
		idx=items_df["probability"].map(lambda x: np.random.uniform()<x)
		items_df=items_df.loc[idx].drop(["probability","Level"],axis=1).sort_values(["Type","Subtype","Name"])
		return items_df