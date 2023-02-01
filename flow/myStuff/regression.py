import dgl
from dgl.data import DGLDataset
import torch
import os
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
from pathlib import Path
import dgl.nn as dglnn
from dgl.dataloading import GraphDataLoader

print("dgl.__version_",dgl.__version__)
#designPath = ""

class DataSetFromYosys( DGLDataset ):
	def __init__( self, mode='train' ):
		self.graphPaths = []
		print("Path.cwd():",Path.cwd())
		for designPath in Path( Path.cwd() ).iterdir():
			if designPath.is_dir():
				print("designPath:",designPath)
				self.graphPaths.append( designPath )
		self.mode = mode
		super().__init__(name='mydata_from_yosys_'+mode)
		

	def _process_single( self, designPath ):
#				nodes_data = pd.read_csv('/home/gudeh/Desktop/OpenROAD-flow-scripts/flow/myStuff/c17/gatesToHeat.csv')
#				edges_data = pd.read_csv('/home/gudeh/Desktop/OpenROAD-flow-scripts/flow/myStuff/c17/DGLedges.csv')
		nodes_data = pd.read_csv( designPath / 'gatesToHeat.csv' )
		edges_data = pd.read_csv( designPath / 'DGLedges.csv')
		edges_src = torch.from_numpy(edges_data['Src'].to_numpy())
		edges_dst = torch.from_numpy(edges_data['Dst'].to_numpy())
		#edge_features = torch.from_numpy(edges_data['Weight'].to_numpy())

		self.graph = dgl.graph((edges_src, edges_dst), num_nodes=nodes_data.shape[0])
		self.graph.ndata['type'] = torch.from_numpy(nodes_data['type'].astype('category').cat.codes.to_numpy())
		#print("self.graph.ndata['type']!",type(self.graph.ndata['type']), "!!!!", self.graph.ndata['type'].shape, self.graph.ndata['type'].type())
		self.graph.ndata['conCount'] = torch.from_numpy(nodes_data['conCount'].to_numpy())
		
		self.graph.ndata['placementHeat'] = torch.from_numpy (nodes_data['placementHeat'].to_numpy())
		self.graph.ndata['powerHeat'] = torch.from_numpy (nodes_data['powerHeat'].to_numpy())
		self.graph.ndata['routingHeat'] = torch.from_numpy (nodes_data['routingHeat'].to_numpy())
		self.graph.ndata['irDropHeat'] = torch.from_numpy (nodes_data['irDropHeat'].to_numpy())
		
		############
		#self.graph.ndata['label'] = self.graph.ndata['placementHeat']
		############
		#self.graph.edata['weight'] = edge_features

		# If your dataset is a node classification dataset, you will need to assign
		# masks indicating whether a node belongs to training, validation, and test set.
#		n_nodes = nodes_data.shape[0]
#		n_train = int(n_nodes * 0.6)
#		n_val = int(n_nodes * 0.2)
#		train_mask = torch.zeros(n_nodes, dtype=torch.bool)
#		val_mask = torch.zeros(n_nodes, dtype=torch.bool)
#		test_mask = torch.zeros(n_nodes, dtype=torch.bool)
#		train_mask[:n_train] = True
#		val_mask[n_train:n_train + n_val] = True
#		test_mask[n_train + n_val:] = True
#		self.graph.ndata['train_mask'] = train_mask
#		self.graph.ndata['val_mask'] = val_mask
#		self.graph.ndata['test_mask'] = test_mask


	
	def process( self ):
		self.graphs = []
		for path in self.graphPaths:
		    graph = self._process_single( path )
		    self.graphs.append( graph )
            
	def __getitem__( self, i ):
		return self.graph

	def __len__( self ):
		#return 1
		return len( self.graphs )
		

class SAGE( nn.Module ):
    def __init__(self, in_feats, hid_feats, out_feats):
        super().__init__()
        self.conv1 = dglnn.SAGEConv(
            in_feats=in_feats, out_feats=hid_feats, aggregator_type='lstm')
        self.conv2 = dglnn.SAGEConv(
            in_feats=hid_feats, out_feats=out_feats, aggregator_type='lstm')

    def forward(self, graph, inputs):
        # inputs are features of nodes
        h = self.conv1(graph, inputs)
        h = F.relu(h)
        h = self.conv2(graph, h)
        return h


def evaluate( model, graph, features, labels, valid_mask, train_mask ):
	model.eval()
	with torch.no_grad():
		logits = model(graph, features)
		logits = logits[valid_mask]
		labelsAux = labels[valid_mask]
		_, indices = torch.max(logits, dim=1)
		correct = torch.sum(indices == labelsAux)
		validAcc = correct.item() * 1.0 / len(labelsAux)
		
		logits = model(graph, features)
		logits = logits[train_mask]
		labels = labels[train_mask]
		_, indices = torch.max(logits, dim=1)
		correct = torch.sum(indices == labels)
		trainAcc = correct.item() * 1.0 / len(labels)
		
		return trainAcc, validAcc
		
def evaluateNoMask( model, graph, features, labels ):
	model.eval()
	with torch.no_grad():
#		logits = model(graph, features)
#		logits = logits[valid_mask]
#		labelsAux = labels[valid_mask]
#		_, indices = torch.max(logits, dim=1)
#		correct = torch.sum(indices == labelsAux)
#		validAcc = correct.item() * 1.0 / len(labelsAux)
		
		logits = model(graph, features)
#		logits = logits[train_mask]
#		labels = labels[train_mask]
		_, indices = torch.max(logits, dim=1)
		correct = torch.sum(indices == labels)
		trainAcc = correct.item() * 1.0 / len(labels)
		
		return trainAcc#, validAcc


def regressionTrain(graph):
#	node_features = graph.ndata['type'][None:1]
	print("\n#################\n### TRAINING ####\n#################\n")
	print("graph.ndata['type']",type(graph.ndata['type']),graph.ndata['type'].shape,graph.ndata['type'].type())
	print("graph.ndata['conCount']",type(graph.ndata['conCount']),graph.ndata['conCount'].shape,graph.ndata['conCount'].type())
	node_features = torch.cat([graph.ndata['type'].float()[:,None], graph.ndata['conCount'].float()[:,None]], dim=1)
	print("node_features",type(node_features),node_features.shape)
	node_labels = graph.ndata['placementHeat'].long()
	node_labels[ node_labels == -1 ] = 0
	train_mask = graph.ndata['train_mask']
	valid_mask = graph.ndata['val_mask']
	test_mask = graph.ndata['test_mask']
	n_features = node_features.shape[1]
	n_labels = int(node_labels.max().item() + 1)

	model = SAGE(in_feats=n_features, hid_feats=100, out_feats=n_labels)
	opt = torch.optim.Adam(model.parameters(), lr=0.03)
	loss_hist = []
	trainAccHist = []
	validAccHist = []
	epochs = 10
	
	for epoch in range( epochs ):
		model.train()
		# forward propagation by using all nodes
		logits = model(graph, node_features)
		# compute loss
		loss = F.cross_entropy( logits[train_mask], node_labels[train_mask] )
		loss_hist.append( loss.item() )
		# compute validation accuracy
		#trainAcc, validAcc  = evaluate( model, graph, node_features, node_labels, valid_mask, train_mask )
		trainAcc  = evaluateNoMask( model, graph, node_features, node_labels )#, valid_mask, train_mask )
		validAcc = 0
		trainAccHist.append( trainAcc )
		validAccHist.append( validAcc )
		# backward propagation
		opt.zero_grad()
		loss.backward()
		opt.step()
	
	print("\n#################\n### END TRAIN ###\n#################\n")
	print( "loss", loss.item(), "trainAcc", trainAcc, "validAcc", validAcc )
	
	fig, ax1 = plt.subplots()
	ax2 = ax1.twinx()
	epochs_list = [i for i in range(epochs)]
	ax1.plot(epochs_list, trainAccHist, label='Training accuracy')
	ax1.plot(epochs_list, validAccHist, label='Validation accuracy')
	ax1.set_ylabel('Accuracy')
	ax1.set_xlabel('epochs')
	ax1.legend()

	ax2.plot(epochs_list, loss_hist, label='Training loss', color = 'g')
#	ax2.plot(epochs_list, val_loss, label='Validation loss')
	ax2.set_ylabel('Loss')
	ax2.set_xlabel('epochs')
	ax2.legend()
	plt.draw()
	plt.show()
	#ax2.savefig(V5_Full_Loss.png)


def printGraph(graph):
#	graph = all_graphs[0][0]
	print( "graph len:\n", graph )
	#graph.ndata['type'] = torch.nn.functional.one_hot(graph.ndata['type'].to(torch.int64))
	#graph.ndata['type'] = torch.from_numpy(graph.ndata['type'].astype('category').cat.codes.to_numpy())

	print("graph:",type(graph))
	print('We have %d nodes.' % graph.number_of_nodes())
	print('We have %d edges.' % graph.number_of_edges())

#	import networkx as nx
#	import matplotlib.pyplot as plt
#	nx_G = graph.to_networkx()
#	pos = nx.kamada_kawai_layout(nx_G)
#	nx.draw(nx_G, pos, with_labels=True, node_color=[[.7, .7, .7]])
#	plt.show()

	print("len graph.ndata:",len(graph.ndata))
	print("type graph.ndata:",type(graph.ndata))

	regressionTrain(graph)
	
	




dataset = DataSetFromYosys(  )
print( "DS size:", len(dataset))
train_dataloader = GraphDataLoader(dataset, batch_size=2)
print( "data_loader", train_dataloader )

	
#regressionTrain( all_graphs[0][0] )

#print("type(all_graphs[0]):", type(all_graphs[0]))
#print("type(all_graphs[0][0]):", type(all_graphs[0][0]))
#print("\n\n\n\n")
#masterGraph = dgl.batch( [all_graphs[0][0], all_graphs[1][0]])#, all_graphs[2][0]] )
#print( "type(masterGraph):",type(masterGraph) )
#print( "masterGraph.batch_size:", masterGraph.batch_size )
#print( "masterGraph.batch_num_nodes:", masterGraph.batch_num_nodes() )
#print( "masterGraph.batch_num_edges:", masterGraph.batch_num_edges() )





#print("len(dataset)", len(dataset))
#print("dataset:", dataset)
#print("dataset[0]:", dataset[0])
#masterGraph = dgl.data.AsNodePredDataset( dataset, [0.8, 0.1, 0.1])#, target_ntype = "type" )
#print( "len(masterGraph):",len(masterGraph) )
#print( "type(masterGraph):",type(masterGraph) )
#print( "type(masterGraph[0]):",type(masterGraph[0]) )



#regressionTrain( masterGraph[0] )

#print("heyy!")




#from dgl.data.ppi import PPIDataset
#train_dataset = PPIDataset(mode='train')
#print("type(train_dataset)", type(train_dataset))


