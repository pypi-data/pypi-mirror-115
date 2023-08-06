#import csv #1.0
import h5py # 2.10.0
import pandas as pd # 0.25.2
#import os
#import sys
#sys.path.append('../')
from supplychainmodulator.datahandling import decBSList
import warnings
warnings.filterwarnings("ignore")

class Datacube:
    '''
    purpose: easy editing of hdf5 database for supply chain modelling
    consists of basic meta data schema for database itself, all 
    folders and datasets.
    basic structure
    database
        - metadata information of all containing folders
        - folder
            - metadata information about folder
            - dataset
                - metadata information about dataset
                - data of dataset
                - axis of dataset

    Possible actions:
    - initialise database: a new hdf5 file created or an existing accessed 
    (see __init__)
    
    - extend the existing basic metadata schema of the database
    (add2ListOfTemplateMDallFolders)
    
    - extend the existing basic metadata schema of an existing folder
    (add2listOfTemplateDataSetMD)
    
    - store the current metadata schema of the database as a 
    template csv file, for later import (createTemplate_MD_Schema_DB_CSV)
    
    - store the current metadata schema of a folder as a 
    template csv file, for later import (createTemplate_MD_Schema_Folder_CSV)
    
    - import csv file with current metadata schema of folder
    and filled out metadata information about containing datasets 
    (importFromCSV_MD_DataForFolder)
    
    -  import csv file with current metadata schema of database
    and filled out metadata information about containing datasets
    (importFromCSV_MD_DataForDB)
        
    - add a folder to the database, incl. a list of metadata information
    based on the current metadataschema (addFolder2ExistingDB)
    
    - add a dataset to an existing folder, incl. a list of metadata information
    based on the current metadataschema (addDataSet2ExistingFolder)
    
    - get an existing dataset from a specific folder in the database
    (getDataFrameFromFolder)
    
    - get metadata information about an existing dataset in the database
    (getMDFromDataSet)
    
    - get metadata information about an existing folder in the database
    (getMDFromFolder)
    
    - get metadata information about the database
    (getMDFromDB)


    '''
    # basic template for mandatory entries for metadata schema
    # if needed add entries in these lists
    # with add2ListOfTemplateMDallFolders or add2listOfTemplateDataSetMD
    listOfTemplateMDallFolders = ['Folder','ID','Title','Description']
    listOfTemplateDataSetMD = ['Dataset','Filename','Format','ID','Title','Rows','Columns','Encoding']
    

    def __init__(self,h5FileName,rights='add'):
        '''
        purpose: initialise the data object

        input:
        :param h5FileName: path to the hdf5 file. If not existing, a new file 
        will be created.
        :param rights(optional): user rights to access this database. 
        'add'(default) user may read/write, if no file by this name exists, the 
        file will be created.
        'new' will overwrite any existing databases (good for testing the database,
        less good for working with it)

        :return: none
        
        example:
        from supplychainmodulator import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        if needed the filename is attached to this data object
        print(testDC.h5FileName)


        '''
        self.h5FileName = h5FileName
        if rights == 'add':
            with h5py.File(h5FileName,'a'):
                pass
        elif rights == 'new':
            with h5py.File(h5FileName,'w'):
                print('new file created...')
        else:
            raise Exception('please choose either \'add\' or \'new\'!')

        
    @classmethod
    def add2ListOfTemplateMDallFolders(cls, listOfAdditionalCategories):
        '''
        purpose: adding a list of metadata categories to the overall metadata structure of the database

        input:
        :param listOfAdditionalCategories: a list of new categories 

        :return: none

        example:
        from supplychainmodulator import mds

        # initialising the datacube operations toolkit
        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # basic md template on creation
        print(testDC.listOfTemplateMDallFolders)
        
        # extend the metadata schema for database
        testDC.add2ListOfTemplateMDallFolders(['db category 1','db category 2','db category 3'])
        
        # check out the CURRENT metadata schema of the database
        print(testDC.listOfTemplateMDallFolders)
        
        '''
        cls.listOfTemplateMDallFolders = cls.listOfTemplateMDallFolders+listOfAdditionalCategories

    @classmethod
    def add2listOfTemplateDataSetMD(cls, listOfAdditionalCategories):
        '''
        purpose: adding a list of metadata categories to the folder meta data

        input:
        :param listOfAdditionalCategories: a list of new categories 

        :return: none

        example:
        from supplychainmodulator import mds

        # initialising the datacube operations toolkit
        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # basic md template on creation
        print(testDC.listOfTemplateDataSetMD)
        
        # extend the metadata schema for database
        testDC.add2listOfTemplateDataSetMD(['folder category 1','folder category 2','folder category 3'])
        
        # check out the CURRENT metadata schema of the database
        print(testDC.listOfTemplateDataSetMD)

        
        '''
        cls.listOfTemplateDataSetMD = cls.listOfTemplateDataSetMD+listOfAdditionalCategories

    
    def createTemplate_MD_Schema_DB_CSV(self,filePathDBSchema):
        '''
        purpose: store the current metadata schema of the database as a 
        template csv file, for later import
        creates a template DataFrame csv file
        containing minimum mandatory metadata information
        which can be filled in csv file 
        and read in via importDBMDSchema


        input:
        :param filePathDBSchema: file path to where the template is 
        stored to a csv file

        :return: none

        example: 
        from supplychainmodulator import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.createTemplate_MD_Schema_DB_CSV('filename.csv')


        '''
        self.filePathDBSchema = filePathDBSchema
        import csv
        with open(self.filePathDBSchema, 'w') as csvfile:
            tempWriter = csv.writer(csvfile, delimiter=';')
            tempWriter.writerow(self.listOfTemplateMDallFolders)
    
    def createTemplate_MD_Schema_Folder_CSV(self,filePathFolderSchema):
        '''
        purpose: creates a template DataFrame csv file
        containing minimum mandatory metadata information
        which can be filled in file 
        and read in via importDBMDSchema

        input:
        :param filePathFolderSchema: file path to where the template is 
        stored to a csv file

        :return: none

        example: 
        from supplychainmodulator import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.createTemplate_MD_Schema_Folder_CSV('filename.csv')

        '''
        self.filePathFolderSchema = filePathFolderSchema
        import csv
        with open(self.filePathFolderSchema, 'w') as csvfile:
            tempWriter = csv.writer(csvfile, delimiter=';')
            tempWriter.writerow(self.listOfTemplateDataSetMD)
              
    def importFromCSV_MD_DataForDB(self,fileName):
        '''
        purpose:     TODO everything
        loads schema dataframe from csv
        needs to have some constraints, see createDBMDSchemaCSV
        check if current md schema is compatible with imported csv
        needs to have some sanity checks either
        create all folders mentioned
        enter into db schema, line by line

        input:
        :param xxx:

        :return: 

        example: 
        from supplychainmodulator import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.createTemplate_MD_Schema_DB_CSV('filename.csv')

    
        '''
        pass
        #with open(self.fileName) ...

    def importFromCSV_MD_DataForFolder(self,fileName):
        '''
        purpose:         TODO everything
        loads schema dataframe from csv
        needs to have some constraints, see createFolderMDSchemaCSV
        check if current md schema is compatible with imported csv
        needs to have some sanity checks either
        create all folders mentioned
        enter into db schema, line by line


        input:
        :param fileName: file path to where the template is 
        stored to a csv file

        :return: dataframe to check given input

        example: 
        from supplychainmodulator import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.createTemplate_MD_Schema_Folder_CSV('filename.csv')


        '''
        pass
        #with open(self.fileName) ...

    def exportSchemaDF2CSV(self, folderPath, dfMD):
        '''
        purpose:    TODO everything
        save csv file to disk
        create folders named in columns "Folder"
        create corresponding folder metadata files

        input:
        :param xxx:

        :return: 

        example:

    
        '''
        self.folderPath = folderPath
        self.dfMD = dfMD


    def addFolder2ExistingDB(self,listOfEntries):
        '''
        purpose:TODO subfolder!
        if md schema exists, add row to table
        create folder md template from column folder
        add md schema to db for all folders

        input:
        :param listOfEntries: list of meta data information. 
        check mandatory fields via listOfTemplateMDallFolders

        :return: none

        example:
        from supplychainmodulator import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        print(testDC.listOfTemplateMDallFolders)
        >>['Folder','ID','Title','Description']

        # add a folder to your database
        myList2FillOut = ['newfolder', '1', 'This is a test', \
            'some kind of description text to describe the reason for the existence of this folder']
        testDC.addFolder2ExistingDB(listOfEntries=myList2FillOut)
   
       
        '''
        if len(listOfEntries) != len(self.listOfTemplateMDallFolders):
            raise Exception('given list of entries incompatible with current metadata schema('\
                +str(len(listOfEntries))+' vs. '+str(len(self.listOfTemplateMDallFolders))+')!')

        with h5py.File(self.h5FileName,'a') as db:
            # check if folder exists already!
            listOfExistingFolders = list(db.keys())
            folderExists = bool(set([listOfEntries[0]]).intersection(set(listOfExistingFolders)))
            if not folderExists:
                db.create_group(listOfEntries[0])
                for index,run in enumerate(self.listOfTemplateMDallFolders):
                    if not db.attrs.__contains__(run): # if this is the first entry
                        myList = []
                    else: # otherwise just add to the list
                        myList = list(db.attrs.__getitem__(run))
                    myList.append(listOfEntries[index])
                    db.attrs[run] = myList
            else:
                raise Exception('This folder already exists!')
            

    def addDataSet2ExistingFolder(self,folderName,listOfDataEntries,datasetDF):
        '''
        purpose: TODO test, subfolder! attach axis of dataframes!
        if md schema exists, add row to metadata table in folder
        add dataset to hdf5, reference to name of Dataset
        add metadata scheme of dataset to folder md schema
        NOTE that onle 2D dataframes are tested to be stored in this DB!

        input:
        :param folderName: name of an existing folder within hdf5 database
        :param listOfDataEntries: list of metadata information of current md schema
        :param datasetDF: a pandas dataframe with information about axis

        :return: 
        
        example:
        from supplychainmodulator import mds
        import pandas as pd

        loc = ['BER','SXF','TXL']

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # creating a folder
        myList2FillOut = ['newfolder', '1', 'This is a test', \
            'some kind of description text to describe the reason for the existence of this folder']
        testDC.addFolder2ExistingDB(listOfEntries=myList2FillOut)

        # Creating dataset
        myData={loc[0]:[1,2,50],loc[1]:[2,1,49],loc[2]:[50,49,1]}
        myDF = pd.DataFrame(myData,index=loc)

        # check current md schema
        print(testDC.listOfTemplateDataSetMD)
        >>['Dataset','Filename','Format','ID','Title','Rows','Columns','Encoding']

        # add dataset to an existing folder
        myList2FillOut = ['distancematrix', 'distmatrix.csv', 'csv', '1', 'Distance matrix', str(len(list(myDF.index))), str(len(list(myDF.columns))), 'utf-8','new cat1','new cat2','new cat3']
        testDC.addDataSet2ExistingFolder(folderName='newfolder', listOfDataEntries=myList2FillOut, datasetDF=myDF)

        
        '''
        self.listOfDataEntries = listOfDataEntries
        self.folderName = folderName 
        self.datasetDF = datasetDF
        if len(self.listOfDataEntries) != len(self.listOfTemplateDataSetMD):
            raise Exception('given list of entries incompatible with current metadata schema!')
        
        # create folder
        # add list of folders with metadata to database
        # attach metadata of folder to folder
        # listOfTemplateDataSetMD = ['Dataset'-0,'Filename'-1,'Format'-2,'ID'-3,'Title'-4,'Rows'-5,'Columns'-6,'Encoding'-7]
        with h5py.File(self.h5FileName,'a') as db:
            # check if folder exists
            listOfExistingFolders = list(db.keys())
            folderExists = bool(set([self.folderName]).intersection(set(listOfExistingFolders)))

            if folderExists:
                # adding dataset to hdf5 file
                nameOfDataSet = listOfDataEntries[0]
                # check if name of data set exists already in this folder
                listOfExistingDataSetsinFolder = list(db[self.folderName].keys())
                DataSetExists = bool(set([nameOfDataSet]).intersection(set(listOfExistingDataSetsinFolder)))

                if not DataSetExists:
                    # store data set in db
                    myD = db[folderName].create_dataset(name=nameOfDataSet,data=datasetDF)
                    
                    # store md attached to dataset in db
                    for index,run in enumerate(self.listOfTemplateDataSetMD):
                        # adding metadata to hdf5 file attached to dataset
                        db[folderName+'/'+nameOfDataSet].attrs[run] = self.listOfDataEntries[index]
                    
                        #adding metadata schema to folder
                        if not db[folderName].attrs.__contains__(run): # if first entry in this folder, create list
                            myList = []
                        else: # otherwise add to existing list
                            myList = list(db[folderName].attrs.__getitem__(run))
                        myList.append(self.listOfDataEntries[index])
                        db[folderName].attrs[run] = myList
                    
                    # store axis information of dataframe attached to dataset
                    try:
                        dtIndex = 'i'
                        db[self.folderName].create_dataset("ScaleRowOfDataSet"+listOfDataEntries[3], \
                            data=self.datasetDF.index.astype(int).values, dtype=dtIndex)
                    except TypeError:
                        dtIndex = h5py.string_dtype(encoding='utf-8')
                        db[self.folderName].create_dataset("ScaleRowOfDataSet"+listOfDataEntries[3], \
                        data=self.datasetDF.index.values, dtype=dtIndex)
                    myD.dims[0].label = self.listOfTemplateDataSetMD[5]
                    myD.dims[0].attach_scale(db[folderName+'/ScaleRowOfDataSet'+listOfDataEntries[3]])

                    try:
                        dtCol = 'i'
                        db[self.folderName].create_dataset("ScaleColOfDataSet"+listOfDataEntries[3], \
                            data=self.datasetDF.columns.astype(int).values, dtype=dtCol)
                    except TypeError:
                        # this only works for py3!
                        dtCol = h5py.string_dtype(encoding='utf-8')
                        db[self.folderName].create_dataset("ScaleColOfDataSet"+listOfDataEntries[3], \
                            data=self.datasetDF.columns.values, dtype=dtCol)
                    # encoding list of strings to list of b-strings (py3 necessity)
                    myD.dims[1].label = self.listOfTemplateDataSetMD[6]
                    myD.dims[1].attach_scale(db[self.folderName+"/ScaleColOfDataSet"+listOfDataEntries[3]])
                    # listOfTemplateDataSetMD = ['Dataset'-0,'Filename'-1,'Format'-2,'ID'-3,'Title'-4,'Rows'-5,'Columns'-6,'Encoding'-7]
                else: 
                    raise Exception('Name of data set already exists in this particular folder, must be unique!')
            else: 
                raise Exception('This folder does NOT exist. Please create a folder by this name!')

    def getDataFrameFromFolder(self,folderName,nameOfDataSet):
        '''
        TODO test
        purpose: retrieve dataset from hdf5 db as pandas data frame

        input:
        :param folderName: name of an existing folder within hdf5 database
        :param nameOfDataSet: the name of the dataset given in list of md schema
        (first element of this list)

        :return: the dataframe with axis(if exist)
        
        example:        
        from supplychainmodulator import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve existing dataset back from database (created by addDataSet2ExistingFolder)
         myDatasetFromhdf5DB = testDC.getDataFrameFromFolder(folderName='newfolder',nameOfDataSet='distancematrix')
        
        
       
        '''
        self.folderName = folderName
        self.nameOfDataSet = nameOfDataSet
              
        with h5py.File(self.h5FileName,'r') as db:
            listOfExistingFolders = list(db.keys())
            folderExists = bool(set([self.folderName]).intersection(set(listOfExistingFolders)))
            if not folderExists:
                raise Exception('Folder name doesnt exist. Please check!')
            try:
                fromDB = db[folderName+'/'+nameOfDataSet]
            except KeyError:
                raise Exception('data set with this name is not stored here!')
            myDF = pd.DataFrame(data=fromDB,\
                    index=decBSList(list(fromDB.dims[0][0])),\
                    columns=decBSList(list(fromDB.dims[1][0])))
        return(myDF)

    def getMDFromDataSet(self,folderName,nameOfDataSet):
        '''
        TODO test
        purpose: retrieve metadata from dataset in hdf5 db

        input:
        :param folderName: name of an existing folder within hdf5 database
        :param nameOfDataSet: the name of the dataset given in list of md schema
        (first element of this list)

        :return: a dataframe(2 column table) of information about an existing dataset
        with headers: MD Names, Content
        
        example:
        from supplychainmodulator import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve existing dataset back from database (created by addDataSet2ExistingFolder)
        print(testDC.getMDFromDataSet(folderName='newfolder',nameOfDataSet='distancematrix'))        

        
        '''
        self.folderName = folderName
        self.nameOfDataSet = nameOfDataSet
        listOfMDNames = []
        listOfMDContents = []
        
        with h5py.File(self.h5FileName,'r') as db:
            try:
                for x in db[folderName+'/'+nameOfDataSet].attrs.__iter__():
                    listOfMDNames.append(x)
                    listOfMDContents.append(db[folderName+'/'+nameOfDataSet].attrs.__getitem__(x))
            except KeyError:
                raise Exception('data set with this name is not stored here!')
        return pd.DataFrame(data={'MD Names':listOfMDNames,'Content':listOfMDContents})

    def getMDFromFolder(self,folderName):
        '''
        purpose:        TODO get like DB otherwise IT WONT WORK!
        retrieve metadata from folder, information about the folder in question
        and which information they contain

        input:
        :param folderName: name of an existing folder within hdf5 database

        :return:  a dataframe(2 column table) of information about an existing dataset
        with headers: MD Names, Content wit list of all datasets
        
        example:
        from supplychainmodulator import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve existing folder back from database (created by addDataSet2ExistingFolder)
        print(testDC.getMDFromFolder(folderName='newfolder'))

        '''
        self.folderName = folderName
        listOfMDNames = []
        listOfMDContents = []
        
        with h5py.File(self.h5FileName,'r') as db:
            try:
                for x in db[folderName].attrs.__iter__():
                    listOfMDNames.append(x)
                    listOfMDContents.append(db[folderName].attrs.__getitem__(x))
            except KeyError:
                raise Exception('data set with this name is not stored here!')
        return pd.DataFrame(data={'MD Names':listOfMDNames,'Content':listOfMDContents})
    
    def getMDFromDB(self):
        '''
        purpose:TODO test with different content and customized metadata schemas
        retrieve metadata from db, information about folders in this database and which information they contain
        returned as pandas dataframe

        input: no parameters needed, as each instance deals with just one databas

        :return: a dataframe (multi-column table) of information about an existing dataset
        with headers based on current md schema (basic schema headers: Description, Folder, ID, Title,)
        
        example:
        from supplychainmodulator import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve md info about database (created by addDataSet2ExistingFolder)        
        print(testDC.getMDFromDB())

        '''
       
        with h5py.File(self.h5FileName,'r') as db:
            try:
                myKeys = [key for key in db.attrs.keys()]
                myVals = [val for val in db.attrs.values()]
            except KeyError:
                raise Exception('data set with this name is not stored here!')
            myDF = pd.DataFrame(columns=myKeys)
            for i,x in enumerate(myVals):
                myDF[myKeys[i]] = list(myVals[i])
        return myDF
