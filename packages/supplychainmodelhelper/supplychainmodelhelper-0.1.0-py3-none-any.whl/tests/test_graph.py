# # %%
# import networkx as nx # V2.4
# import h5py
# import numpy as np
# import time
# import sys
# sys.path.append('../')
# from supplychainmodulator.datahandling import decBS, decBSList
#
# #############################################################################################
# # DEFINE
# # PARAMETERS         AND
# # DATA SOURCE
# #
# #############################################################################################
# # define filename for hdf5 data base
# # intro to hdf5, see: https://en.wikipedia.org/wiki/Hierarchical_Data_Format
# # (groups = folders)
# filenameH5 = './tests/test.hdf5'
#
#
# #############################################################################################
#
# #############################################################################################
# # PREPROCESSING
# # PARAMETERS DERIVED FROM DATA SOURCE AND PARAMETERS
# #############################################################################################
#
# # for performance measure only, no purpose in model
# startTiming = time.time()
#
#
# # LOCATIONS
# # from hdf5 db
# with h5py.File(filenameH5,'r') as db:
#     # get me the names of all the folders in my db
#     folderNames = list(db.keys())
#
#     # get into the folder where locations dataset is stored
#     dsetH5 = db['Other/locations']
#
#     # define matrix with the content of dsetH5 and its datatype
#     locationsData = np.zeros(dsetH5.shape, dtype=dsetH5.dtype)
#
#     # get the metadata info from attached schema
#     locationsID = list(map(int,list(dsetH5.dims[0][0])))
#     cols= decBSList(list(dsetH5.dims[1][0]))
#     namesOfLocationsID = cols.index('Name')
#
#     # variable locationsData (defined above) filled with info from db
#     dsetH5.read_direct(locationsData)
#
#     # make a list out of the metadata
#     namesOfLocationList = decBSList(list(locationsData[:,namesOfLocationsID]))
#
#     # PRODUCTS
#     dsetH5 = db['Other/products']
#     productNameList = list(dsetH5.dims[0][0])
#
#     # ACTORS
#     dsetH5 = db['Other/actors']
#     actorList = list(dsetH5.dims[0][0])
#
#     #more ACTORS Warehouses
#     warehouseList = [x for x in list(db['Warehouses']) if not x.startswith('Scale')]
# ############################################################################################
# # %%
#
