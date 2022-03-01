import pandas as pd
import numpy as np #np.nan
import glob
import os
import time
from datetime import datetime, timedelta


class gate:
	name=""
	x0=0.0
	y0=0.0
	x1=0.0
	y1=0.0
	width=0.0
	height=0.0
	
	def __init__(self):
		#TODO transform this guys into a dict={str:[]}, str is the heat name
		self.heat_placement=[]
		self.heat_power=[]
		self.heat_routing=[]
		self.heat_irdrop=[]
	
	def __str__(self):
		message=self.name+"\t("+'%.1f'%self.x0+";"+'%.1f'%self.y0+";"+'%.1f'%self.x1+";"+'%.1f'%self.y1+"),w-"+'%.1f'%self.width+",h-"+'%.1f'%self.height
		message=message+"\tplacement-"
		for value in self.heat_placement:
			message=message+'%.1f'%value+";"
		message=message+"\tpower-"
		for value in self.heat_power:
			message=message+'%.1f'%value+";"
		message=message+"\trouting-"
		for value in self.heat_routing:
			message=message+'%.1f'%value+";"
		message=message+"\tirdrop-"
		for value in self.heat_irdrop:
			message=message+'%.1f'%value+";"
		return message
	
class heatBbox:
	name=""
	x0=0.0
	y0=0.0
	x1=0.0
	y1=0.0
	width=0.0
	height=0.0
	value=0.0
	
	def __str__(self):
		message=self.name+"\t("+'%.1f'%self.x0+";"+'%.1f'%self.y0+";"+'%.1f'%self.x1+";"+'%.1f'%self.y1+"),w-"+'%.1f'%self.width+",h-"+'%.1f'%self.height+",v-"+'%.1f'%self.value
		return message


root="./myStuff"
all_projects = [name for name in os.listdir(root) if os.path.isdir(os.path.join(root,name))]
print("all_projects directories:",all_projects)
for projects in all_projects:
	projects=root+"/"+projects
	print (projects)
	if os.path.exists(projects+"/outDGLcells.csv"):
		os.remove(projects+"/outDGLcells.csv")
#	heat_csvs = glob.glob(projects+"/*.csv")
	heat_csvs = glob.glob(projects+"/[!DGL]*.csv")
#	feature_csvs= glob.glob(projects+"/DGL*.csv")
#	print("all YOSYS csvs in project",len(feature_csvs),feature_csvs)
	print("all HEAT csvs in project",len(heat_csvs),heat_csvs)
	position_files=[myfile for myfile in heat_csvs if "gatesPosition" in myfile]
	positions_df=pd.read_csv(position_files[0])
	print("this length should be == 1:",len(position_files),position_files)

	print(positions_df.head)
	all_gates={}
	for index,row in positions_df.iterrows():
		myGate=gate()
		myGate.name=row["Name"]
		myGate.x0=row["xMin"]
		myGate.y0=row["yMin"]
		myGate.x1=row["xMax"]
		myGate.y1=row["yMax"]
		myGate.width=row["xMax"]-row["xMin"]
		myGate.height=row["yMax"]-row["yMin"]
#		all_gates.append(myGate)
		all_gates[row["Name"]]=myGate
	print("Loaded gates position objects!")
	print("size:",len(all_gates),flush=True)
	
	heat_files=[myfile for myfile in heat_csvs if "gates" not in myfile]
	for heat_file in heat_files:
		start_time = int(datetime.now().timestamp())
		if "placement" in heat_file:
			heat_type="placement"
		elif "power" in heat_file:
			heat_type="power"
		elif "routing" in heat_file:
			heat_type="routing"
		elif "irdrop" in heat_file:
			heat_type="irdrop"
		print("loading:",heat_type, "(file:",heat_file,")")
		heat_df=pd.read_csv(heat_file)
		print("heat frame shape:",heat_df.shape)
		heat_df=heat_df.drop(heat_df[heat_df.value==0].index)
		print("heat frame shape:",heat_df.shape,"after removing 0's")
		all_heats=[]
		for index,row in heat_df.iterrows():
#			print("index",index)
			myHeat=heatBbox()
			myHeat.name=heat_type
			myHeat.x0=row["x0"]
			myHeat.y0=row["y0"]
			myHeat.x1=row["x1"]
			myHeat.y1=row["y1"]
			myHeat.value=row["value"]
			myHeat.width=row["x1"]-row["x0"]
			myHeat.height=row["y1"]-row["y0"]
			all_heats.append(myHeat)
		print("Loaded heat objects!",flush=True)
		
#		for heat in all_heats:
#			print(heat)
		if heat_type=="placement":
			for key,mygate in all_gates.items():
				for myheat in all_heats:
#						print(mygate.x0,"<=",myheat.x1,mygate.x0 <= myheat.x1,"and",mygate.x1,">=",myheat.x0,mygate.x1 >= myheat.x0,"and",mygate.y1,">=",myheat.y0, mygate.y1 >= myheat.y0, mygate.y0 <= myheat.y1,"and",mygate.y0,"<=",myheat.y1)
					if mygate.x0 <= myheat.x1 and mygate.x1 >= myheat.x0 and mygate.y1 >= myheat.y0 and mygate.y0 <= myheat.y1:
						mygate.heat_placement.append(myheat.value)
						if len(mygate.heat_placement) > 4:
							print("ERROR, impossible for a gate to be in more than 1 bbox?",mygate.name)
		if heat_type=="power":
			for key,mygate in all_gates.items():
				for myheat in all_heats:
					if len(mygate.heat_power) <= 4:
#						print(mygate.x0,"<=",myheat.x1,mygate.x0 <= myheat.x1,"and",mygate.x1,">=",myheat.x0,mygate.x1 >= myheat.x0,"and",mygate.y1,">=",myheat.y0, mygate.y1 >= myheat.y0, mygate.y0 <= myheat.y1,"and",mygate.y0,"<=",myheat.y1)
						if mygate.x0 <= myheat.x1 and mygate.x1 >= myheat.x0 and mygate.y1 >= myheat.y0 and mygate.y0 <= myheat.y1:
							mygate.heat_power.append(myheat.value)
							
		if heat_type=="routing":
			for key,mygate in all_gates.items():
				for myheat in all_heats:
					if len(mygate.heat_routing) <= 4:
#						print(mygate.x0,"<=",myheat.x1,mygate.x0 <= myheat.x1,"and",mygate.x1,">=",myheat.x0,mygate.x1 >= myheat.x0,"and",mygate.y1,">=",myheat.y0, mygate.y1 >= myheat.y0, mygate.y0 <= myheat.y1,"and",mygate.y0,"<=",myheat.y1)
						if mygate.x0 <= myheat.x1 and mygate.x1 >= myheat.x0 and mygate.y1 >= myheat.y0 and mygate.y0 <= myheat.y1:
							mygate.heat_routing.append(myheat.value)
		if heat_type=="irdrop":
			for key,mygate in all_gates.items():
				for myheat in all_heats:
					if len(mygate.heat_irdrop) <= 4:
#						print(mygate.x0,"<=",myheat.x1,mygate.x0 <= myheat.x1,"and",mygate.x1,">=",myheat.x0,mygate.x1 >= myheat.x0,"and",mygate.y1,">=",myheat.y0, mygate.y1 >= myheat.y0, mygate.y0 <= myheat.y1,"and",mygate.y0,"<=",myheat.y1)
						if mygate.x0 <= myheat.x1 and mygate.x1 >= myheat.x0 and mygate.y1 >= myheat.y0 and mygate.y0 <= myheat.y1:
							mygate.heat_irdrop.append(myheat.value)
		
		finish_time = int(datetime.now().timestamp())
		print("time for all gates:",(finish_time-start_time),"-",heat_type,flush=True)
#	for key,mygate in all_gates.items():
#		print(mygate)
	df_cells=pd.read_csv(projects+"/DGLcells.csv")	
	df_cells["Hplacement"]=-1
	df_cells["Hpower"]=-1
	df_cells["Hrouting"]=-1
	df_cells["Hirdrop"]=-1
	present_cell=0
	for key,mygate in all_gates.items():
		if mygate.name in df_cells.values:
			present_cell+=1
			df_cells.loc[df_cells.Name==mygate.name,"Hplacement"]=max(mygate.heat_placement,default=0)
			df_cells.loc[df_cells.Name==mygate.name,"Hpower"]=max(mygate.heat_power,default=0)
			df_cells.loc[df_cells.Name==mygate.name,"Hrouting"]=max(mygate.heat_routing,default=0)
			df_cells.loc[df_cells.Name==mygate.name,"Hirdrop"]=max(mygate.heat_irdrop,default=0)			
#			print ("gate",mygate.name," is present in df")
#		else:
#			print("gate",mygate.name," is NOT!! present in df")
	df_cells.set_index('Id')
	print("#cells in DGLcells.csv:",df_cells.shape[0],"(from Yosys)")
	print("#cells in gatePositions:",positions_df.shape[0],"(from TCL provided in OpenROAD discussion)")
	print("#cells in last heat_df:",heat_df.shape[0],"last heat:",heat_type,"(from gui::dump command)")
	print("#cells in both heatmap and DGLScells.csv:",present_cell)
	
	df_cells.to_csv(projects+"/outDGLcells.csv",index=False)
	print("envirment variable:",os.environ['DESIGN_NAME'])

