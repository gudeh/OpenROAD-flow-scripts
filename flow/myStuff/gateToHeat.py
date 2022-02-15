import pandas as pd
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
	all_csvs = glob.glob(projects+"/*.csv")
	print(len(all_csvs),all_csvs)
	gate_files=[myfile for myfile in all_csvs if "gates" in myfile]
	gate_df=pd.read_csv(gate_files[0])
	print("this length should be ==1 >>",len(gate_files),gate_files)

	print(gate_df.head)
	all_gates=[]
	for index,row in gate_df.iterrows():
		myGate=gate()
		myGate.name=row["Name"]
		myGate.x0=row["xMin"]
		myGate.y0=row["yMin"]
		myGate.x1=row["xMax"]
		myGate.y1=row["yMax"]
		myGate.width=row["xMax"]-row["xMin"]
		myGate.height=row["yMax"]-row["yMin"]
		all_gates.append(myGate)
	print("Loaded gates position objects!")
	print("size:",len(all_gates))
	
	heat_files=[myfile for myfile in all_csvs if "gates" not in myfile]
	for heat_file in heat_files:
		start_time = int(datetime.now().timestamp())
		if "placement" in heat_file:
			heat_type="placement"
		elif "power" in heat_file:
			heat_type="power"
		elif "routing" in heat_file:
			heat_type="routing"
		elif "irdrop" in heat_file:
			heat_type="IRdrop"
		print("loading:",heat_type, "(file:",heat_file,")")
		heat_df=pd.read_csv(heat_file)
		print("heat frame shape:",heat_df.shape)
		heat_df=heat_df.drop(heat_df[heat_df.value==0].index)
		print("heat frame shape:",heat_df.shape,"after removing 0s")
		all_heats=[]
		for index,row in heat_df.iterrows():
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
		print("Loaded gates objects!")
		
		for heat in all_heats:
			print(heat)
		if heat_type=="placement":
			for mygate in all_gates:
				for myheat in all_heats:
#						print(mygate.x0,"<=",myheat.x1,mygate.x0 <= myheat.x1,"and",mygate.x1,">=",myheat.x0,mygate.x1 >= myheat.x0,"and",mygate.y1,">=",myheat.y0, mygate.y1 >= myheat.y0, mygate.y0 <= myheat.y1,"and",mygate.y0,"<=",myheat.y1)
					if mygate.x0 <= myheat.x1 and mygate.x1 >= myheat.x0 and mygate.y1 >= myheat.y0 and mygate.y0 <= myheat.y1:
						mygate.heat_placement.append(myheat.value)
						if len(mygate.heat_placement) > 4:
							print("ERROR, impossible for a gate to be in more than 1 bbox?",mygate.name)
		if heat_type=="power":
			for mygate in all_gates:
				for myheat in all_heats:
					if len(mygate.heat_power) <= 4:
#						print(mygate.x0,"<=",myheat.x1,mygate.x0 <= myheat.x1,"and",mygate.x1,">=",myheat.x0,mygate.x1 >= myheat.x0,"and",mygate.y1,">=",myheat.y0, mygate.y1 >= myheat.y0, mygate.y0 <= myheat.y1,"and",mygate.y0,"<=",myheat.y1)
						if mygate.x0 <= myheat.x1 and mygate.x1 >= myheat.x0 and mygate.y1 >= myheat.y0 and mygate.y0 <= myheat.y1:
							mygate.heat_power.append(myheat.value)
							
		if heat_type=="routing":
			for mygate in all_gates:
				for myheat in all_heats:
					if len(mygate.heat_routing) <= 4:
#						print(mygate.x0,"<=",myheat.x1,mygate.x0 <= myheat.x1,"and",mygate.x1,">=",myheat.x0,mygate.x1 >= myheat.x0,"and",mygate.y1,">=",myheat.y0, mygate.y1 >= myheat.y0, mygate.y0 <= myheat.y1,"and",mygate.y0,"<=",myheat.y1)
						if mygate.x0 <= myheat.x1 and mygate.x1 >= myheat.x0 and mygate.y1 >= myheat.y0 and mygate.y0 <= myheat.y1:
							mygate.heat_routing.append(myheat.value)
		if heat_type=="irdrop":
			for mygate in all_gates:
				for myheat in all_heats:
					if len(mygate.heat_irdrop) <= 4:
#						print(mygate.x0,"<=",myheat.x1,mygate.x0 <= myheat.x1,"and",mygate.x1,">=",myheat.x0,mygate.x1 >= myheat.x0,"and",mygate.y1,">=",myheat.y0, mygate.y1 >= myheat.y0, mygate.y0 <= myheat.y1,"and",mygate.y0,"<=",myheat.y1)
						if mygate.x0 <= myheat.x1 and mygate.x1 >= myheat.x0 and mygate.y1 >= myheat.y0 and mygate.y0 <= myheat.y1:
							mygate.heat_irdrop.append(myheat.value)
		
		finish_time = int(datetime.now().timestamp())
		print("time for all gates:",(finish_time-start_time),"-",heat_type)
	for mygate in all_gates:
		print(mygate)
			

	#for mygate in all_gates:
	#	print(mygate.name,mygate.x0,mygate.y0,mygate.x1,mygate.y1)
