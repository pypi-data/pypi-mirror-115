# %%
import sys
import pandas as pd

sys.path.append('../')
from supplychainmodulator.mds import Datacube

test = Datacube('./test1.hdf5')

#test.createSchemaCSV('./test.csv')

print('\nold set of MD: ')
print(str(test.listOfTemplateMDallFolders))
test.add2ListOfTemplateMDallFolders(['sonder','super','ttt'])
print('\nnew set of MD: ')
print(str(test.listOfTemplateMDallFolders))

tt = ['test','IDhh','mtTitle','myDescription','hjh','jtztz','ggg']
#test.addFolder2ExistingDB(tt)
tt2 = ['test2','IDhh','mtTitle','myDescription2','hjh2','jfddstztz','ggg2']
#test.addFolder2ExistingDB(tt2)
print('\nnew set of MD for folder: '+tt2[0])
# #print(str(test.listOfEntries))

# myDatasetMD = ['testds','test.csv','csv','1','my test','3','2','utf-8']
# myD = {'Manfred': [1,2,3],'Thomas':[3,4,5]}
# thisDF = pd.DataFrame(data=myD,index=['a','b','c'])
# test.addDataSet2ExistingFolder(tt[0],myDatasetMD,thisDF)
# #test.addDataSet2ExistingFolder(tt[0],myDatasetMD,thisDF)
# print('\ndata set md info for dataset: '+myDatasetMD[0])
# print(str(test.listOfDataEntries))


# print('\nget me info about the database')
# print(test.getMDFromDB())

# print('\nGet me Folder: '+tt[0])
# mdDF = test.getMDFromFolder(tt[0])

# print('\ni want to see my md from folder: '+tt[0]+' and dataset: '+mdDF['Content'][1][0])
# print(test.getMDFromDataSet(tt[0],mdDF['Content'][1][0]))

# print('\nmy Dataframe, please:')
# print(test.getDataFrameFromFolder(tt[0],mdDF['Content'][1][0]))





# %%
# %%
