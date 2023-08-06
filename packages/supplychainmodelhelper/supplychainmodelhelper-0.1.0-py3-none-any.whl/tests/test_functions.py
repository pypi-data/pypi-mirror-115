# from supplychainmodulator import playground as pg
# from supplychainmodulator import datahandling as dh
# from supplychainmodulator import mds
# from supplychainmodulator import graphoperations as go
#
# import h5py # 2.10.0
# import csv
# import pandas as pd # 0.25.2
# import os.path
# import unittest as ut
#
# def test_haversine():
#     assert pg.haversine(52.370216, 4.895168, 52.520008,13.404954) == 945793.4375088713
#
#
# def test_importDataFromFolder():
#     assert dh.importDataFromFolder("./data/metadata/","folderMD.csv","./data/rawData.hdf5") == True
#
#
# def test_combineActorBrand():
#     assert go.combineActorBrand("test",["one","two"]) == ["test_one","test_two"]
#
# def test_decBSList():
#     assert dh.decBSList([b'string1',b'string2']) == ["string1","string2"]
#     assert dh.decBSList(['string1','string2']) == ["string1","string2"]
#
# def test_decBS():
#     assert dh.decBS(b'string1') == "string1"
#     assert dh.decBS('string1') == "string1"
#
# def test_Datainit():
#     myfname = './testDC.hdf5'
#     testDC = mds.Datacube(myfname)
#     assert os.path.isfile(myfname)
#     assert testDC.fileName == myfname
#
# def test_createMDSchema():
#     myfname = './testDC.hdf5'
#     testDC = mds.Datacube(myfname)
#     testDF = {'col1': [1,2], 'col2':[3,4]}
#     assert testDC.createMDSchema(testDF) == testDF
#
# # def test_addFolder2ExistingDB():
# #     # TODO check if this works correctly!
# #     # TODO how to check if this is written corecctly?!
# #     myfname = './testDC.hdf5'
# #     testDC = mds.Datacube(myfname)
# #     with ut.TestCase.assertRaises(Exception):
# #         testDC.addFolder2ExistingDB(['testDataset','testFilename','testFormat','testID',\
# #         'testTitle','testRows','testColumns','testEncoding'])
# #
# #     testDC.addFolder2ExistingDB()
#
# # def test_addDataSet2ExistingFolder():
# #     # TODO check if this works correctly!
# #     myfname = './testDC.hdf5'
# #     testDC = mds.Datacube(myfname)
# #     testDC.addFolder2ExistingDB(testDC.listOfTemplateMDallFolders)
# #
# #     with ut.TestCase.assertRaises(Exception):
# #         testDC.addDataSet2ExistingFolder(myfname,'test',['mytest'])
# #
# #     testDF = {'col1': [1,2], 'col2':[3,4]}
# #     testDC.addDataSet2ExistingFolder(myfname,\
# #         'test',\
# #             testDC.listOfTemplateFolderMD,\
# #                 testDF)
# #
# # # def more tests