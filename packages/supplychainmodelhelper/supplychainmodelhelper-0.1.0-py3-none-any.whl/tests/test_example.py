from supplychainmodulator.datahandling import importDataFromFolder
import csv
import os
import h5py
import pandas as pd # 0.25.2
#mymy = importDataFromFolder("./data/metadata/","folderMD.csv","./data/rawData.hdf5")

#print(mymy)



fileInputPath = "./data/metadata/"
fileInMetadataName = "folderMD.csv"
foldername = "Distances"

# metaDataFile = csv.DictReader(open(fileInputPath+foldername+"/"+foldername+"MD.csv"),delimiter=';')
# folderMD = csv.DictReader(open(fileInputPath+fileInMetadataName),delimiter=';')
# #print(os.path.exists(fileInputPath+foldername+"/"+foldername+"MD.csv"))

# # writing the hdf5 structure
# with h5py.File("test.hdf5",'w') as db:
#     ####################################################
#     # creating the structure from meta data schema table
#     ####################################################
#     # getting the metadata from each metadata table in each of the folders as described in fileFolderLoc
#     for row in folderMD:
#         myAttrs = list(row.keys())        
#         # creating the folders and look out for subfolders
#         if not row['Subfolder']:
#             db.create_group(row['Folder'])
#             for run in myAttrs:
#                 # attach all info to metadata schema
#                 if run != 'Folder' and run != 'Subfolder':
#                     db[row['Folder']].attrs[run] = row[run]

#         # creating the subfolders(aka subgroups) inside hdf5 db if existing in metadata file
#         if row['Subfolder']:
#             db[row['Folder']].create_group(row['Subfolder'])

#             for run in myAttrs:
#                 if run != 'Folder' and run != 'Subfolder':
#                     db[row['Folder']+'/'+row['Subfolder']].attrs[run] = row[run]
#     for foldername in db:
#         print(foldername)
#         metaDataFile = csv.DictReader(open(fileInputPath+foldername+"/"+foldername+"MD.csv"),delimiter=';')
#         for row in metaDataFile:
#             # read in the data set: NEEDS to have index and column header in csv file
#             #print(row)
#             dataSet = pd.read_csv(fileInputPath+foldername+"/"+row['Filename'],header=0,sep=';',index_col=0,encoding=row['Encoding'],dtype='str')        
                        
#             # create the hdf5 dataset and store it in the hdf5-file
#             dt = h5py.string_dtype(encoding='utf-8')
#             d5 = db[foldername].create_dataset(row['Dataset'], data=dataSet, dtype=dt)
            
#             # attach metadata information to newly created data set
#             myAttrs = list(row.keys())
#             for run in myAttrs:
#                 if run != 'Dataset':
#                     db[foldername+'/'+row['Dataset']].attrs[run]=row[run]
            

#             # attach dimension scale from csv file, ASSUMING it's always a 2d table...
#             # TODO make it dynamical, so that the reader recognizes the format!
#             # has a unique ID, given that in the MD-files this ID is unique (filewise), as well!
#             # TODO currently unique ID is given in filename --> make it internal UID!
#             try:
#                 dtIndex = 'i'
#                 db[foldername].create_dataset("ScaleRowOfDataSet"+row['ID'], data=dataSet.index.astype(int).values, dtype=dtIndex)
#             except TypeError:
#                 # this only works for py3!
#                 dtIndex = h5py.string_dtype(encoding='utf-8')
#                 db[foldername].create_dataset("ScaleRowOfDataSet"+row['ID'], data=dataSet.index.values, dtype=dtIndex)
    
#             # attach the header row and header columne of the table as meta data info
#             # TODO automatic recognition of header -> cell data type analysis (header = string, data=not string)
#             d5.dims[0].label = row['Rows']
#             d5.dims[0].attach_scale(db[foldername+"/ScaleRowOfDataSet"+row['ID']])
            

#             try:
#                 dtCol = 'i'
#                 db[foldername].create_dataset("ScaleColOfDataSet"+row['ID'], data=dataSet.columns.astype(int).values, dtype=dtCol)
#             except TypeError:
#                 # this only works for py3!
#                 dtCol = h5py.string_dtype(encoding='utf-8')
#                 db[foldername].create_dataset("ScaleColOfDataSet"+row['ID'], data=dataSet.columns.values, dtype=dtCol)
            
#             # encoding list of strings to list of b-strings (py3 necessity)
#             d5.dims[1].label = row['Columns']
#             d5.dims[1].attach_scale(db[foldername+"/ScaleColOfDataSet"+row['ID']])
