# %%

''' if you need an explanation on how to use a particular function, please have a look at 
help(function)

example:
help(go.combineActorBrand)
or 
help(mds.Datacube)

'''
import sys
sys.path.append('../')
from supplychainmodulator import graphoperations as go


import pandas as pd

prod = ['milk','beer','schnaps']
act = ['producer','consumer','warehouse','store']
loc = ['BER','SXF','TXL']

# adding a brand to some actors
newActors = go.combineActorBrand(actor='warehouse',brand=['ALDI','REWE','LIDL'])
act.remove('warehouse')
act.extend(newActors)
print('new list of actors')
print(act)

# Erschaffen des graphen myNW
myNW = go.createGraph(listOfActors=act,listOfLocations=loc,listOfProducts=prod)


# get Node IDs, wann immer einer der standard parameter (actor,location,product) nicht mitgegeben
# wird, wird angenommen, dass alle gemeint sind
print('\nMeine Produzenten:')
producerIDs = go.getListOfNodeIDs(myNW, actors=['producer'])
print(producerIDs)

print('\nMeine Product Beer:')
beerIDs = go.getListOfNodeIDs(myNW, products=['beer'])
print(beerIDs)

print('\nMeine Konsumenten von Schnaps:')
consumerOfSchnapsIDs = go.getListOfNodeIDs(myNW, products=['schnaps'],actors=['producer'])
print(consumerOfSchnapsIDs)

# tuples of (Node ID, attribute content)
print('\nMeine Produzenten wohnen hier:')
print(go.getNodeIDswAttr(myNW,nameOfAttr='location',listOfNodeIDs=producerIDs))

print('\nMeine Produzenten produzieren:')
print(go.getNodeIDswAttr(myNW,nameOfAttr='product',listOfNodeIDs=producerIDs))

# adding new attributes
listOfAGS = ['01111','01112','01113','01111','01112','01113','01111','01112','01113']
didItWork = go.addAttr2ExistingNodes(myNW, listOfNodeIDs=producerIDs, nameOfAttr='ags', listOfAttr=listOfAGS)
print('Ist es im Graph gespeichert: '+str(didItWork))

# check if new attribute is getable
print('\nMeine Produzenten haben folgende AGS:')
print(go.getNodeIDswAttr(myNW,nameOfAttr='ags',listOfNodeIDs=producerIDs))

#get me the IDs of the edges between producers and consumers of schnaps
myEdgeIDs = go.getEdgeID(myNW, outgoingNodes=producerIDs, incomingNodes=consumerOfSchnapsIDs)
print('\nMeine Liste von Tuples (outID,inID):')
print(myEdgeIDs)

# füge hinzu transport
print('\nSpeichere neue Tranport infos:')
listOfShipping = [10,1,2000]
didItWork2 = go.addAttr2Edges(myNW, listOfEdgeIDs=myEdgeIDs, listOfContent=listOfShipping, attr='weight')
print('Ist es im Graph gespeichert: '+str(didItWork2))

# gib mir alle edges wo 'weight' drin steht
print('\nWas steht denn in allen Edges die WEIGHT haben drin?')
print(go.getEdgesAttr(myNW, attr = 'weight'))
print('Was steht denn drin bei einem?')
print(go.getEdgesAttr(myNW, attr = 'weight', listOfEdgeIDs = [myEdgeIDs[1]]))

# gib mir alle edges wo 'weight' drin steht, als Tuple mit (EdgeID,attribute) = (NodeOutID,NodeInID, attribute)
print('\nWo steht denn was in allen Edges die WEIGHT haben drin?')
print(go.getEdgeIDswAttr(myNW, attr = 'weight'))
print('Wo steht denn was drin bei einem?')
print(go.getEdgeIDswAttr(myNW, attr = 'weight', listOfEdgeIDs = [myEdgeIDs[1]]))



################################################################
# baue distanzen ein:
senderIDs = go.getListOfNodeIDs(myNW, actors=['producer'],products=['milk'])
receiverIDs = go.getListOfNodeIDs(myNW, actors=['consumer'],products=['milk'])
allcombIDs1,allcombIDs2 = go.getAllCombinations(senderIDs,receiverIDs,order='1st')
myEdges4Graph = go.getEdgeID(myNW,allcombIDs1,allcombIDs2)
sendingMilk = [10,50,40]
receivingMilk = [30,30,40]
go.addAttr2ExistingNodes(myNW,senderIDs,'output',sendingMilk)
go.addAttr2ExistingNodes(myNW,receiverIDs,'input',receivingMilk)

# building distance matrix from scratch
print('\nCreating Distance matrix')
myData={loc[0]:[1,2,50],loc[1]:[2,1,49],loc[2]:[50,49,1]}
myDF = pd.DataFrame(myData,index=loc)
print(myDF)
didItWork3 = go.addAttr2Edges(myNW,myEdges4Graph, myDF.values.flatten(),attr='distance')
print('\nWas it added to the graph:'+str(didItWork3))
print('Give me a list of all (outNodeID,inNodeID,distance):')
print(go.getEdgeIDswAttr(myNW, attr = 'distance',listOfEdgeIDs=myEdges4Graph))

print('\n Give me the average transport distances for these fake data points')
myTDs = go.calcPotTransportDistances(myNW, listOfSenderIDs=senderIDs, listOfReceiverIDs=receiverIDs, nrOfValues=5)
print(myTDs)

print('This is the distance matrix that was entered by the user')
print(go.getDistMatrix(myNW, listOfSenderIDs=senderIDs, listOfReceiverIDs=receiverIDs, edgeattrDistName='distance'))

print('Run the gravity model with given transport distance and return the flow')
print(go.hymanModel(myNW, listOfSenderIDs=senderIDs, listOfReceiverIDs=receiverIDs, transportDistance=myTDs[0], tolerance = 0.01))
#furnessModel(SCGraph: Graph, listOfSenderIDs: list, listOfReceiverIDs: list, beta: float, edgeattrDistName: str, distanceModel: str):

# which attribute may i ask for
print('\nWas gibt es alles für Attribute in meinem Netzwerk?')
print(go.getExistingAttrs(myNW, gtype = 'nodes'))
print(go.getExistingAttrs(myNW, gtype = 'edges'))

# independent of node IDs but is created for this purpose
print('\nConvert a list of tuples')
print(myEdges4Graph)
print('to different lists')
list1,list2 = go.convertLoT2NTs(myEdges4Graph)
print(list1)
print(list2)
print('and gluing those lists back together')
print(go.convertTup2LoT(list1,list2))

print('\nApplying the proxyModel:')
nationalProduction = 100.
proxynatProduction = 10.
proxyregProduction = [2,4,2]
regionalProduction = go.proxyModel(inputNr=nationalProduction, proxyData=proxyregProduction, proxyNr=proxynatProduction)
print(regionalProduction)
print('creating list of tuples for input for proxymodel')
proxyregProdWithNodeIDs = go.convertTup2LoT(senderIDs,proxyregProduction)
regionalProduction = go.proxyModel(inputNr=nationalProduction, proxyData=proxyregProdWithNodeIDs, proxyNr=proxynatProduction)
print(regionalProduction)

###############################
# HDF5
###############################
from supplychainmodulator import mds
from supplychainmodulator import datahandling as dh

# initialising the datacube operations toolkit
myfname = './testDCnew.hdf5'
testDC = mds.Datacube(myfname,'new')

# uncomment if you really want to import from an existing folder, otherwise dont
'''
######################################
path2DataFolder = '../data/metadata/'#folder where your data set lies
######################################
mdFile = 'folderMD.csv'

# import existing folder with specific structure into specific hdf5 format for this toolkit
print('\n\nimport data structure, please uncomment if wanted\n')

didItWork4 = dh.importDataFromFolder(fileInputPath=path2DataFolder, fileInMetadataName=mdFile, fileOutputName=myfname)
print(didItWork4)
'''

#create new database from scratch
#just by initialising the datacube already has some attributes
# a simple metadata schema of the folders
print('\n\n################################################')
print('if needed the filename is attached to this data object:')
print(testDC.h5FileName)
print('check out the BASIC metadata schema of the database')
print(testDC.listOfTemplateMDallFolders)
print('check out the basic metadata schema of the folders if created')
print(testDC.listOfTemplateFolderMD)
print('\n')
print('extend the metadata schema for database')
print(testDC.add2ListOfTemplateMDallFolders(['db category 1','db category 2','db category 3']))
print('check out the CURRENT metadata schema of the database')
print(testDC.listOfTemplateMDallFolders)
print('\n')
print('extend the metadata schema for the folders')
print(testDC.add2ListOFTemplateFolderMD(['folder category 1','folder category 2','folder category 3']))
print('check out the CURRENT metadata schema of the folders if created')
print(testDC.listOfTemplateFolderMD)
print('\n')
print('export current metadata schema of database TEMPLATE to csv (write in csv then import later)')
filePathDBSchema = 'dbschemaTemplate.csv'
testDC.createDBMDSchemaCSV(filePathDBSchema)
print('\n')
print('export current metadata schema of folder TEMPLATE to csv (write in csv then import later)')
filePathfolderSchema = 'folderschemaTemplate.csv'
testDC.createFolderMDSchemaCSV(filePathfolderSchema)
print('\n')
print('import current metadata schema of database TEMPLATE from csv (write in csv then import later)')
print('NOT IMPLEMENTED YET')
print('\n')
print('import current metadata schema of folder TEMPLATE from csv (write in csv then import later)')
print('NOT IMPLEMENTED YET')
print('\n')
print('add a folder to your database')
myList2FillOut = ['newfolder', '1', 'This is a test', 'some kind of description text to describe the reason for the existence of this folder','content for category 1','content for category 2','content for category 3']
testDC.addFolder2ExistingDB(listOfEntries=myList2FillOut)
print('\n')
print('add another folder to your database')
myMDList2FillOut = ['data', '2', 'This is another test', 'some kind of description text to describe the reason for the existence of this folder','about the same content for category 1','much more content for category 2','more content for category 3']
testDC.addFolder2ExistingDB(listOfEntries=myMDList2FillOut)
print('\n')
print('add a dataset to your database')
myMDList2FillOut = ['distancematrix', 'distmatrix.csv', 'csv', '1', 'Distance matrix', str(len(list(myDF.index))), str(len(list(myDF.columns))), 'utf-8','new cat1','new cat2','new cat3']
testDC.addDataSet2ExistingFolder(folderName='newfolder', listOfDataEntries=myMDList2FillOut, datasetDF=myDF)
print('\n')
print('get dataset in form of dataframe')
myDatasetFromhdf5DB = testDC.getDataFrameFromFolder(folderName='newfolder',nameOfDataSet='distancematrix')
print(myDatasetFromhdf5DB)
print('\n')
print('get metadata information of database')
print(testDC.getMDFromDB())
print('get metadata information of folder')
print(testDC.getMDFromFolder(folderName='newfolder'))
print('get metadata information of dataset')
print(testDC.getMDFromDataSet(folderName='newfolder',nameOfDataSet='distancematrix'))







# %%
