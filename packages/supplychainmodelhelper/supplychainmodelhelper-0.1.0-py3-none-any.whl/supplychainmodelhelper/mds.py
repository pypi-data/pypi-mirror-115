#import csv #1.0
import h5py # 2.10.0
import pandas as pd # 0.25.2
import os.path
#import sys
#sys.path.append('../')
from supplychainmodelhelper.datahandling import decBSList
import warnings
#warnings.filterwarnings("ignore")

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
    Please NOTE that only 1 schema exists at a time for the
    database in question. This schema exists to get easy
    access to existing folders and scan through the database rather
    quickly.
    At this point there is no plan to add multiple md schemas
    to 1 database.
    (add2TemplateMDofDB)
    
    - extend the existing basic metadata schema of an existing dataset
    Please NOTE that only 1 schema exists at a time for the
    dataset in question. This schema exists to get easy
    access to existing datasets and scan through the database rather
    quickly.
    At this point there is no plan to add multiple md schemas
    to 1 database.
    Further note that folders have a similar md schema as the dataset
    itself. The difference is that in any folder the md schema for
    ALL datasets inside the folder is summarized. See getMDFromFolder
    and getMDFromDataSet.
    (add2TemplateMDofDataset)
    
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

    - change metadata information of dataset, folder, database
    (setNewMD2Dataset,setNewMD2Folder,setNewMD2DB)

    - remove meta data categories from md schema
    (removeFolderMD,removeDatasetMD)

    '''
    # basic template for mandatory entries for metadata schema
    # if needed add entries in these lists
    # with add2TemplateMDofDB or add2TemplateMDofDataset
    h5Filename = 'defaultDB.hdf5'
    listOfTemplateMDofDB = ['Folder','ID','Title','Description']
    listOfTemplateMDofDataset = ['Dataset','Filename','Format','ID','Title','Rows','Columns','Encoding']
    

    # TODO test in combination with other functions
    def __init__(self, h5Filename, rights='add'):
        '''
        purpose: initialise the data object

        input:
        :param h5Filename(optional): path to the hdf5 file. If not existing, a new file
        will be created. default filename is 'defaultDB.hdf5'
        :param rights(optional): user rights to access this database. 
        'add'(default) user may read/write, if no file by this name exists, the 
        file will be created.
        'new' will overwrite any existing databases (good for testing the database,
        less good for working with it).
        Also on initialisation of this data object the given hdf5 database will be accessed
        and the md schema from the db overwrites the default md schema

        :return: none
        
        example:
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        if needed the filename is attached to this data object
        print(testDC.h5Filename)



        ===============================================================================================

        '''

        self.overwriteFileName(h5Filename)
        if rights == 'add':
            with h5py.File(h5Filename,'a') as db:
                # check md schema of existing db
                if len(list(db.keys())) > 0:
                    checkCurrentMDschema=list(self.getMDFromDB().columns)
                    allCategories = [True if i in self.listOfTemplateMDofDB else False \
                                            for i in checkCurrentMDschema]
                    # check if more categories exist in db than in basic md schema
                    if not all(allCategories):
                        # get index of new categories
                        addCat = [f for f,x in enumerate(allCategories) if not x]
                        self.listOfTemplateMDofDB+=list(map(checkCurrentMDschema.__getitem__,addCat))
                    newCategories = []
                    for folder in db.keys():
                        for dataset in db[folder].keys():
                            checkCurrentMDschema = list(self.getMDFromDataSet(folder,dataset).columns)
                            allCategories = [True if i in self.listOfTemplateMDofDB else False \
                                             for i in checkCurrentMDschema]
                            if not all(allCategories):
                                addCat = [f for f, x in enumerate(allCategories) if not x]
                                newCatThisTime = list(map(checkCurrentMDschema.__getitem__, addCat))
                                newCategories = newCategories+newCatThisTime
                    if newCategories != newCatThisTime:
                        warnings.warn('Please be advised, different meta data schemas for different datasets is untested!')
                    self.listOfTemplateMDofDataset+=newCategories

        elif rights == 'new':
            with h5py.File(self.h5Filename,'w'):
                print('new file created...')
        else:
            raise Exception('please choose either \'add\' or \'new\'!')

    @classmethod
    def overwriteFileName(cls,fileName):
        cls.h5Filename = fileName

    # TODO test in combination with other functions
    # TODO write self test to test new db sync functionality
    @classmethod
    def add2TemplateMDofDB(cls, listOfAdditionalCategories, sure=False):
        '''

        if folder/dataset in db exists, add this new element to all existing
        give user warning that missing entries need to be added to dataset by
        other function
        purpose: adding a list of metadata categories to the overall metadata
        structure of the database

        input:
        :param listOfAdditionalCategories: a list of new categories
        :param sure(optional) only asked for if database named in initialisation, already
        contains folders.
        New categories in db will have the note 'no entry yet'


        :return: none

        example:
        from supplychainmodelhelper import mds

        # initialising the datacube operations toolkit
        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # basic md template on creation
        print(testDC.listOfTemplateMDofDB)
        
        # extend the metadata schema for database
        testDC.add2TemplateMDofDB(['db category 1','db category 2','db category 3'])
        
        # check out the CURRENT metadata schema of the database
        print(testDC.listOfTemplateMDofDB)
 


        ===============================================================================================       
        '''
        # new md schema is built
        newMDschema = cls.listOfTemplateMDofDB[:]+listOfAdditionalCategories[:]

        # check if existing folders need update
        newCat = [i for i in newMDschema if i not in cls.listOfTemplateMDofDB]

        # check with db
        with h5py.File(cls.h5Filename,'a') as db:
            # do folders exist? if so, check if element exists and if not update it
            if not sure:
                if len(list(db.keys())) > 0:
                    warnings.warn('Please be advised. \
                    \nYou are about to change the md schema on existing db.\
                    \nRepeat this command with the flag sure=True, if you\'re really sure about this')
                else:
                    # counting doubles
                    if len(newMDschema) == len(set(newMDschema)):
                        cls.listOfTemplateMDofDB = newMDschema[:]
                    else:
                        warnings.warn('At least one element was already in the md schema. \
                        \nRemoving the redundancy!')
                        cls.listOfTemplateMDofDB = list(set(newMDschema[:]))
            # user is sure about what he/she is doing
            if sure:
                if len(list(db.keys())) > 0:
                    # go through every folder
                    for run in newCat:
                        # for each folder 1 entry exists
                        if not db.attrs.__contains__(run):  # if this is the first entry
                            db.attrs[run] = ['no entry yet']*len(newCat)
                    # counting doubles
                    if len(newMDschema) == len(set(newMDschema)):
                        cls.listOfTemplateMDofDB = newMDschema[:]
                    else:
                        warnings.warn('Warning: At least one element was already in the md schema, removing the redundancy.')
                        cls.listOfTemplateMDofDB = list(set(newMDschema[:]))
                else:
                    warnings.warn('Warning: You set the flag \'sure\'=True, but no entries are to be find in database! Nothing done.')

    # TODO test in combination with other functions
    # TODO write self test to test new db sync functionality
    @classmethod
    def add2TemplateMDofDataset(cls, listOfAdditionalCategories, sure=False):
        '''
        purpose: adding a list of metadata categories to the folder meta data

        input:
        :param listOfAdditionalCategories: a list of new categories 
        :param sure(optional) only asked for if an hdf5 contains folder or dataset
        and the needs to be updated afterwards. New categories in db will have the
        note 'no entry yet'

        :return: none

        example:
        from supplychainmodelhelper import mds

        # initialising the datacube operations toolkit
        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # basic md template on creation
        print(testDC.listOfTemplateMDofDataset)
        
        # extend the metadata schema for database
        testDC.add2TemplateMDofDataset(['data category 1','data category 2','data category 3'])
        
        # check out the CURRENT metadata schema of the database
        print(testDC.listOfTemplateMDofDataset)

        # if dataset are added, the flag 'sure' needs to be set to 'True' otherwise
        # change requests are ignored
        testDC.addFolder2ExistingDB(['thisnewFolder', '2', 's', 'Descripcvdxction'])

        ===============================================================================================
        
        '''
        newMDschema = cls.listOfTemplateMDofDataset+listOfAdditionalCategories

        # check if existing folders need update
        newCat = [i for i in newMDschema if i not in cls.listOfTemplateMDofDataset]

        # check with db
        with h5py.File(cls.h5Filename,'a') as db:
            # do folders exist? if so, check if element exists and if not update it
            if not sure:
                if len(list(db.keys())) > 0:
                    warnings.warn('Please be advised. You are about to change the md schema on existing db.\
                        \nRepeat this command with the flag sure=True, if you\'re really sure about this')
                else:
                    # counting doubles
                    if len(newMDschema) == len(set(newMDschema)):
                        cls.listOfTemplateMDofDataset = newMDschema
                    else:
                        warnings.warn('at least one element was already in the md schema, removing the redundancy.')
                        cls.listOfTemplateMDofDataset = list(set(newMDschema))

            # user is sure about what he/she is doing
            if sure:
                if len(list(db.keys())) > 0:
                    # go through every folder
                    for folder in db.keys():
                        for run in newCat:
                            # for each folder 1 entry exists
                            if not db[folder].attrs.__contains__(run):  # if this is the first entry
                                db[folder].attrs[run] = 'no entry yet'
                        for ds in db[folder].keys():
                            for run in newCat:
                                if not db[folder+'/'+ds].attrs.__contains__(run):
                                    db[folder+'/'+ds].attrs[run] = 'no entry yet'
                    # counting doubles
                    if len(newMDschema) == len(set(newMDschema)):
                        cls.listOfTemplateMDofDataset = newMDschema
                    else:
                        warnings.warn('at least one element was already in the md schema.\
                            \nRemoving the redundancy.')
                        cls.listOfTemplateMDofDataset = list(set(newMDschema))
                else:
                    warnings.warn('Warning: You set the flag \'sure\'=True, but no entries are to be find in database! Nothing done.')

    # TODO test in combination with other functions
    # TODO write self test to test new db sync functionality
    # TODO some elements (name, id) cant be removed
    @classmethod
    def removeFromTemplateMDofDB(cls, attr2remove, sure=False):
        '''
        purpose: 
        If no folders are inserted yet to the database, the md schema
        wil be updated with no further warning. This can be undone
        by the function add2TemplateMDofDB.
        If at least 1 folder in db exists, remove this category from all
        existing folders in db. The user gets a warning if the flag 'sure'
        is NOT set to true.

        input:
        :param attr2remove: can be a list or a str
        :param sure(optional): set True, if database exists already and existing
        entries are to be removed

        :return: none

        example:
        from supplychainmodelhelper import mds

        # initialising the datacube operations toolkit
        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # basic md template on creation
        print(testDC.listOfTemplateMDofDB)

        # extend the metadata schema for database
        testDC.add2TemplateMDofDB(['db category 1','db category 2','db category 3'])

        # check out the CURRENT metadata schema of the database
        print(testDC.listOfTemplateMDofDB)

        # extend the metadata schema for database
        # can be a list
        testDC.removeFromTemplateMDofDB(['db category 1','db category 2'])
        # or a string
        testDC.removeFromTemplateMDofDB('db category 3')

        # check out the CURRENT metadata schema of the database
        print(testDC.listOfTemplateMDofDB)


        ===============================================================================================
        '''
        if not sure: 
            with h5py.File(cls.h5Filename,'r') as db:
                # do folders exist? if so, check if element exists and if not update it
                if len(list(db.keys())) > 0:
                    # dont do anything if folders exists and the flag sure is not set
                    # -> probably user did something wrong
                    rem = False

                    if isinstance(attr2remove, str):
                        if db.attrs.__contains__(attr2remove):
                            warnings.warn('Please be advised. '+str(attr2remove)+' is already entered into the database.\nRepeat this command with the flag sure=True, if you\'re really sure about this')
                        else:
                            warnings.warn('Attribute '+str(attr2remove)+' not found in database. Please check spelling!')
                    elif isinstance(attr2remove, list):
                        for el in attr2remove:
                            if db.attrs.__contains__(el):
                                warnings.warn('Please be advised. '+str(el)+' is already entered into the database.\nRepeat this command with the flag sure=True, if you\'re really sure about this')
                            else:
                                warnings.warn('Attribute '+str(el)+' not found in database. Please check spelling!')
                else:
                    # no folders exist and sure is not set to True by hand of user
                    # -> probably ok, but if not, user may undo this by add2TemplateMDofDB
                    rem = True
        if sure:
            with h5py.File(cls.h5Filename,'a') as db:
                # user is sure about what he/she is doing
                if len(list(db.keys())) > 0:
                    # probably ok, so go ahead and update class variable
                    # with md schema
                    rem = True
                    if isinstance(attr2remove, str):
                        if db.attrs.__contains__(attr2remove):
                            del db.attrs[attr2remove]
                    elif isinstance(attr2remove, list):
                        for el in attr2remove:
                            if db.attrs.__contains__(el):
                                del db.attrs[el]
                else:
                    # probably the user did something wrong,
                    # so dont do anythind
                    rem = False
                    warnings.warn('You set the flag sure, even if no database could be found. Either read documentation more carfully, or something weird happened. For security, nothing removed.')

        # rem is true if sure is False AND no existing entries are in db -> entries removed
        # rem is false if sure is True AND no existing entries are in db -> something weird happened or
        #   user didnt read the doc
        # rem is false if sure is False AND existing entries are in db -> user tries to edit db without
        # being sure
        # rem is true if sure is True AND existing entries are in db -> entries removed and synced with db

        if rem:
            # check if input is a list or a str
            if isinstance(attr2remove, str):
                if not attr2remove in cls.listOfTemplateMDofDB:
                    raise Exception('Given string is not an element of the current meta data schema!')
                else:
                    cls.listOfTemplateMDofDB.remove(attr2remove)
            elif isinstance(attr2remove, list):
                for a in attr2remove:
                    if not a in cls.listOfTemplateMDofDB:
                        raise Exception('Element ' + str(a) + ' is not an element of the current meta data schema!')
                    cls.listOfTemplateMDofDB.remove(a)
            else:
                raise Exception('Input is neither list nor string! Nothing removed!')

    # TODO test in combination with other functions
    # TODO write self test to test new db sync functionality
    # TODO some elements (name, id) cant be removed
    @classmethod
    def removeElementTemplateDataSetMD(cls, attr2remove, sure=False):
        '''
        purpose: removing either 1 element as string or multiple elements of
        metadata categories from ALL datasets.
        There are no multiple schemas for different datasets.
        Might be added later, if pressure is high.

        input:
        :param attr2remove: a str or a list of existing categories

        :return: none

        example:
        from supplychainmodelhelper import mds

        # initialising the datacube operations toolkit
        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # basic md template on creation
        print(testDC.listOfTemplateMDofDataset)

        # extend the metadata schema for database
        testDC.add2TemplateMDofDataset(['folder category 1','folder category 2','folder category 3'])

        # check out the CURRENT metadata schema of the database
        print(testDC.listOfTemplateMDofDataset)

        # removing 1 item
        testDC.removeElementTemplateDataSetMD('folder category 2')
        print(testDC.listOfTemplateMDofDataset)

        # removing more items
        testDC.removeElementTemplateDataSetMD(['folder category 1','folder category 3'])
        print(testDC.listOfTemplateMDofDataset)


        ===============================================================================================

        '''
        if not sure: 
            with h5py.File(cls.h5Filename,'r') as db:
                # do folders exist? if so, check if element exists and if not update it
                if len(list(db.keys())) > 0:
                    # dont do anything if folders exists and the flag sure is not set
                    # -> probably user did something wrong
                    rem = False

                    for folder in db.keys():
                        if isinstance(attr2remove,str):
                            if db[folder].attrs.__contains__(attr2remove):
                                warnings.warn('Please be advised. '+str(attr2remove)+' is already entered into the database.\nRepeat this command with the flag sure=True, if you\'re really sure about this')
                            else:
                                warnings.warn('Attribute '+str(attr2remove)+' not found in database. Please check spelling!')                                
                        elif isinstance(attr2remove,list):
                            for el in attr2remove:
                                if db[folder].attrs.__contains__(el):
                                    warnings.warn('Please be advised. '+str(el)+' is already entered into the database.\nRepeat this command with the flag sure=True, if you\'re really sure about this')
                                else:
                                    warnings.warn('Attribute '+str(el)+' not found in database. Please check spelling!')
                else:
                    # no folders exist and sure is not set to True by hand of user
                    # -> probably ok, but if not, user may undo this by add2TemplateMDofDB
                    rem = True

        # optional flag default is False
        if sure:
            with h5py.File(cls.h5Filename,'a') as db:
                # do folders exist? if so, check if element exists and if not update it
                if len(list(db.keys())) > 0:
                    # probably ok, so go ahead and update class variable
                    # with md schema
                    rem = True

                    for folder in db.keys():
                        if isinstance(attr2remove,str):
                            if db[folder].attrs.__contains__(attr2remove):
                                del db[folder].attrs[attr2remove]
                                print('attribute removed from folder: '+folder)
                            else:
                                warnings.warn('Attribute '+str(attr2remove)+' not found in database. Please check spelling!')                                
                            for ds in db[folder].keys():
                                if db[folder+'/'+ds].attrs.__contains__(attr2remove):
                                    del db[folder+'/'+ds].attrs[attr2remove]
                                    print('attribute removed from dataset: '+ds)
                        elif isinstance(attr2remove,list):
                            for el in attr2remove:
                                if db[folder].attrs.__contains__(el):
                                    del db[folder].attrs[el]
                                    print('attribute removed from folder: '+folder)
                                else:
                                    warnings.warn('Attribute '+str(el)+'in folder '+folder+' not found in database. Please check spelling!')
                                for ds in db[folder].keys():
                                    if db[folder+'/'+ds].attrs.__contains__(el):
                                        del db[folder+'/'+ds].attrs[el]
                                        print('attribute removed from dataset: '+ds)
                                    else:
                                        warnings.warn('Attribute '+str(el)+'in folder '+folder+' in dataset '+ds+' not found in database. Please check spelling!')
                else:
                    # probably the user did something wrong,
                    # so dont do anythind
                    rem = False
                    warnings.warn('You set the flag sure, even if no database could be found. Either read documentation more carfully, or something weird happened.')


        # rem is true if sure is False AND no existing entries are in db -> entries removed
        # rem is false if sure is True AND no existing entries are in db -> something weird happened or
        #   user didnt read the doc
        # rem is false if sure is False AND existing entries are in db -> user tries to edit db without
        # being sure
        # rem is true if sure is True AND existing entries are in db -> entries removed and synced with db

        if rem:
            if isinstance(attr2remove, str):
                if not attr2remove in cls.listOfTemplateMDofDataset:
                    raise Exception('Given string is not an element of the current meta data schema!')
                else:
                    cls.listOfTemplateMDofDataset.remove(attr2remove)
            elif isinstance(attr2remove, list):
                for a in attr2remove:
                    if not a in cls.listOfTemplateMDofDataset:
                        raise Exception('Element ' + str(a) + ' is not an element of the current meta data schema!')
                    cls.listOfTemplateMDofDataset.remove(a)
            else:
                raise Exception('input is neither list nor string')

    # TODO test
    # TODO write self test to test new db sync functionality
    # TODO check if ID is unique
    def editMDofDataset(self,folder: str,dataset: str, category: str, content: str):
        '''
        purpose:
        adding a new category to md schema of dataset is done by
        the function add2TemplateMDofDataset (see example).
        Using this function only editing of EXISTING md categories is supported.
        Adding a new category means an update to all datasets, while
        this function only edits (or adds) content to 1 dataset at a time.

        This function checks if all inputs (folder, dataset, category) exists
        before editing the field.

        NOTE that the folder md data is updated as well, since the folder md
        is just a summary of what is in the folder.

        TODO:
        Future updates may have the option of having the variable dataset as a list
        and content as a list, so that multiple entries may be done at the same
        time.

        TODO:
        Is a flag for overwriting existing content necessary?

        input:
        :param folder: existing folder in db (str) - assumed all datasets are in
        given folder
        :param datasets: existing dataset (str)
        :param category: existing category (str) for changing 1 category
        at a time
        :param content: corresponding content existing category for changing

        :return: none

        example: 
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        # adding folders to database
        newFolderMD = ['newfolder','1','A new Folder','A very cool description']
        myNewDB.addFolder2ExistingDB(newFolderMD)

        # adding dataset to folder
        loc = ['BER','TXL','SXF']
        myData={loc[0]:[1,2,50],loc[1]:[2,1,49],loc[2]:[50,49,1]}
        myDF = pd.DataFrame(myData,index=loc)
        dataMD = ['distanceMatrix','no filename','pandas df','1','distance matrix','3','3','utf-8']
        myNewDB.addDataSet2ExistingFolder(newFolderMD[0],dataMD,myDF)

        # adding new md schema to dataset (user gets error, because at least 1 dataset is stored
        # to database
        myNewDB.add2TemplateMDofDataset(['Creator','time of creation'])

        # adding new md schema to dataset, being sure
        myNewDB.add2TemplateMDofDataset(['Creator','time of creation'],sure=True)

        # get md info about dataset
        print(myNewDB.getMDFromDataSet(folder='newfolder',dataset='distanceMatrix'))

        # editing dataset
        myNewDB.editMDofDataset(folder='newfolder',dataset='distanceMatrix', \
            category='Creator', content='Marcel')
        myNewDB.editMDofDataset(folder='newfolder',dataset='distanceMatrix', \
            category='time of creation', content='today')


        ===============================================================================================
    
        '''             
        with h5py.File(self.h5Filename,'a') as db:
            if len(list(db.keys()))>0:
                if folder in db.keys():
                    if dataset in db[folder].keys():
                        if db[folder].attrs.__contains__(category):
                            if db[folder+'/'+dataset].attrs.__contains__(category):
                                # edit folder md entry in list
                                whereItBelongs = list(db[folder].attrs['Dataset']).index(dataset)
                                db[folder].attrs[category] = list(db[folder].attrs[category])[whereItBelongs]
                                # edit dataset md
                                db[folder+'/'+dataset].attrs[category] = content
                            else:
                                raise Exception('category does not exist in dataset!')
                        else:
                            raise Exception('category does not exist in folder!')
                    else:
                        raise Exception('dataset does not exist!')
                else:
                    raise Exception('folder does not exist!')
            else:
                raise Exception('no folders yet!')
            


            if isinstance(category,str) and isinstance(content,str):
                if db.attrs.__contains__(category):
                    db.attrs[category] = content
            elif isinstance(category,list) and isinstance(content,list):
                for it,el in enumerate(category):
                    if db.attrs.__contains__(el):
                        db.attrs[el] = content[it]
            else:
                raise Exception('Both \'category\' and \'content\' must be either str OR list. No mixing up please!')

    # TODO test
    # TODO write self test to test new db sync functionality
    # TODO check if ID is unique
    # TODO name shouldnt be editable or sync with db
    # TODO:
    #   Future updates may have the option of having the variable dataset as a list
    #   and content as a list, so that multiple entries may be done at the same
    #   time.
    # TODO:
    #   Is a flag for overwriting existing content necessary?
    def editMDofDB(self, folder, category: str, content):
        '''
        purpose:
        Adding a new category to the MD schema of the database is done by
        the function add2TemplateMDofDB (see example).
        Using this function only editing of EXISTING md categories is supported.
        Adding a new category means an update to md data of database, while
        This function only edits (or adds) content to 1 entry of the database
        at a time.

        TODO:
        Future updates may have the option of having the variable dataset as a list
        and content as a list, so that multiple entries may be done at the same
        time.

        TODO:
        Is a flag for overwriting existing content necessary?


        input:
        :param folder: the folder for which the content is for (str or list)
        :param categories: existing categories for changing (str) - 1 category at a time
        :param content: corresponding content existing category and (str or list of)
        folders for changing (str or list) - same dimension as folder

        :return: 

        example: 
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        # add 3 folders
        folder1 = ['test','1','a title','a description']
        folder2 = ['anothertest','2','another title','a new description']
        folder3 = ['yetanothertest','3','yet another title','also new description']
        myNewDB.addFolder2ExistingDB(folder1)
        myNewDB.addFolder2ExistingDB(folder2)
        myNewDB.addFolder2ExistingDB(folder3)

        # add categories without being sure (gets an error, because user wasnt sure
        myNewDB.add2TemplateMDofDB(['source','year','help'])

        # add categories with being sure
        myNewDB.add2TemplateMDofDB(['source','year','help'],sure=True)

        # edit new entries
        folderNames = [folder1[0],folder2[0],folder3[0]]
        myContent = ['Astronomische Nachrichten','Zentralblatt Mathematik','FMJ']
        myNewDB.editMDofDB(folder=folderNames, category='source', content=myContent)
        # edit other entries
        myContent = ['2009','2021','2017']
        myNewDB.editMDofDB(folder=folderNames, category='year', content=myContent)

        #see changes
        print(myNewDB.getMDfromDB())




        ===============================================================================================
    
        '''
        existingFolders = list(self.getMDFromDB()['Folder'])
        with h5py.File(self.h5Filename,'a') as db:
            # check if folder is str and content is str
            # as they are to be connected
            if isinstance(folder,str) and isinstance(content,str):
                # if this attribute exists in database, go ahead

                if db.attrs.__contains__(category) and folder in existingFolders:
                    # get attribute of category and look up the index where folder is
                    existingContent = db.attrs[category]
                    myFolderIndex = list(db.attrs['Folder']).index(folder)
                    # replace existing content with new content
                    existingContent[myFolderIndex] = content
                    # store replacement in attributes of database
                    db.attrs[category] = existingContent
                else:
                    raise Exception('Either the category'+category+' or the folder'+folder+' could not be found in database!')
            elif isinstance(folder,list) and isinstance(content,list):
                if len(folder) != len(content):
                    raise Exception('both list of folders and list of content need to be the same length!')
                for it,el in enumerate(content):
                    if db.attrs.__contains__(category) and folder[it] in existingFolders:
                        # get attribute of category and look up the index where folder is
                        existingContent = list(db.attrs[category])
                        if len(existingContent)==0:
                            raise Exception(str(category)+' should result in a list with at least one entry. Error in database md schema!')
                        myFolderIndex = list(db.attrs['Folder']).index(folder[it])
                        # replace existing content with new content
                        existingContent[myFolderIndex] = el
                        # store replacement in attributes of database
                        db.attrs[category] = existingContent
                    else:
                        raise Exception('Either category '+category+' or folder '+str(folder[it])+' could not be found in database!')
            else:
                raise Exception('Both \'category\' and \'content\' must be either str OR list. No mixing up please!')

    # TODO test
    def exportTemplateMDSchemaofDB2CSV(self,filePathDBSchema):
        '''
        purpose:
        store the current metadata schema of the database as a
        template csv file, for later import
        creates a template DataFrame csv file
        containing minimum mandatory metadata information
        which can be filled in csv file 
        and read in via importMDSchemaofDBfromCSV


        input:
        :param filePathDBSchema: file path to where the template is 
        stored to a csv file

        :return: none

        example: 
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.exportTemplateMDSchemaofDB2CSV('myBasicMDschemaofDB.csv')

        myNewDB.add2TemplateMDofDB(['a new category','another new one','not another one of these')

        myNewDB.exportTemplateMDSchemaofDB2CSV('expandedMDschemaofDB.csv')



        ===============================================================================================

        '''
        self.filePathDBSchema = filePathDBSchema
        import csv
        with open(self.filePathDBSchema, 'w') as csvfile:
            tempWriter = csv.writer(csvfile, delimiter=';')
            tempWriter.writerow(self.listOfTemplateMDofDB)


    # TODO test
    def exportTemplateMDSchemaofDataset2CSV(self,filePathFolderSchema):
        '''
        purpose:
        stores the current metadata schema into an csv file.
        information about dataset may be added and later import in via
        importMDSchemaofDatasetFromCSV.


        input:
        :param filePathFolderSchema: file path to where the template is 
        stored to a csv file

        :return: none

        example: 
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.createTemplate_MD_Schema_Folder_CSV('myBasicMDschemaforAllDatasets.csv')

        # adding more categories
        myNewDB.add2TemplateMDofDataset(['something old','something new')

        myNewDB.createTemplate_MD_Schema_Folder_CSV('myBasicMDschemaforAllDatasets.csv')


        ===============================================================================================
        '''
        self.filePathFolderSchema = filePathFolderSchema
        import csv
        with open(self.filePathFolderSchema, 'w') as csvfile:
            tempWriter = csv.writer(csvfile, delimiter=';')
            tempWriter.writerow(self.listOfTemplateMDofDataset)


    # TODO test in combination with other stuff
    # TODO check if add2folder doesnt mess with sync the db
    # TODO check if md schema is in agreement with db loaded
    # TODO check if ID is unique
    # TODO check if user imports new md data into existing db -> use case?
    # TODO set flag sure, for user that wants to overwrite current md schema
    def importMDDataofDBfromCSV(self,csvFileName):
        '''
        purpose:
        User may export current md schema with function
        exportTemplateMDSchemaofDB2CSV to a csv file, then
        edit csv file and then import the content into the
        Datacube.
        NOTE that database should be freshly initialised and NOT
        contain any other data than an extended md schema up to this point.
        This case has not been tested.

        MD schema of csv and current md schema of db (via add2TemplateMDofDB)
        need to be identical (returns error if doesnt fit).
        I.e. the first row of the csv file should contain the
        fields of the md schema.
        All folders are to be created in the database. The name
        and the ID need to be unique (is enforced!).

        User may want to import self created csv:
        If csv file is not created by exportTemplateMDSchemaofDB2CSV
        the separator used should be a ';'.

        input:
        :param csvFileName: filename of the csv file, filled in by user

        :return: 

        example: 
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.exportTemplateMDSchemaofDB2CSV('filename.csv')

        #...
        # user sees this in 'filename.csv'
        'Folder';'ID';'Title';'Description'
        #...
        # user fills in the fields : csv mock up of 'filename.csv'
        'Folder';'ID';'Title';'Description'
        'test1';'1';'my first Title';'my first description'
        'test2';'2';'my second Title';'my second description'
        'test3';'3';'my third Title';'my third description'
        'test4';'4';'my fourth Title';'my fourth description'

        #...

        myNewDB.importMDSchemaofDBfromCSV('filename.csv')

        # show me the new folders incl. md schema
        print(myNewDB.getMDFromDB())




        ===============================================================================================
    
        '''
        myTable = pd.read_csv(csvFileName, delimiter=';')
        
        for row in myTable.index:
            currentListOfEntries = []
            for el in self.listOfTemplateMDofDB:
                currentListOfEntries.append(myTable[el][row])
            self.addFolder2ExistingDB(currentListOfEntries)

    # TODO test
    # TODO write self test to test new db sync functionality
    # TODO check if add2folder doesnt mess with sync the db
    # TODO check if md schema is in agreement with db loaded
    # TODO check if ID is unique
    # TODO if folder doesnt exist in db, create folder!
    def importMDDataofDatasetFromCSV(self,folderName,csvFileName):
        '''
        purpose:
        User may export current md schema with function
        exportTemplateMDSchemaofDataset2CSV to a csv file, then
        edit csv file and then import the content into the
        Datacube.

        Checks if current md schema is compatible with imported csv.
        Checks if input parameter folderName exists as folder in database.
        This function imports all assiociated files named in respective
        md schema and imports them automatically into the database.
        Search for files either in directory where csv file with md data is
        stored or in a subdirectory named 'folderName'. Returns error if
        neither option is good.

        User may want to import self created csv:
        If csv file is not created by exportTemplateMDSchemaofDB2CSV
        the separator used should be a ';'.
        


        input:
        :param folderName: name of existing folder in database
        if data files are stored in subdirectory, it should have
        the same name
        :param fileName: file path to where the template is 
        stored to a csv file. Filenames given in md schema should
        match the filenames on disk.

        :return: dataframe to check given input

        example: 
        from supplychainmodelhelper import mds
        myNewDB = mds.Datacube('test.hdf5','new')

        myNewDB.addFolder2ExistingDB(['myfolder'])

        myNewDB.exportTemplateMDSchemaofDataset2CSV('filename.csv')

        print(myNewDB.

        #...
        # user sees this in 'filename.csv'
        'Dataset';'Filename';'Format';'ID';'Title';'Rows';'Columns';'Encoding'
        # ...
        # user fills in information
        'Dataset';'Filename';'Format';'ID';'Title';'Rows';'Columns';'Encoding'
        'data1';'data1.csv';'csv';'1';'my first title';'4';'3';'utf-8'
        'data2';'data2.csv';'csv';'2';'my new title';'12';'31';'utf-8'
        'data3';'data3.csv';'csv';'3';'my other title';'123';'13';'utf-8'
        # ...

        myNewDB.importMDDataofDatasetFromCSV('myfolder','filename.csv')
        print(myNewDB.getMDFromFolder('myfolder'))



        ===============================================================================================

        '''
        myTable = pd.read_csv(csvFileName, delimiter=';')
        csvDir = os.path.dirname(os.path.abspath(csvFileName))


        # check if given foldername exists
        dbMD = self.getMDFromDB()
        existingFolders = [dbMD['Folder'][i] for i in dbMD.index]
        if not folderName in existingFolders:
            raise Exception('Please use function \'addFolder2ExistingDB\' to add folder with metadata schema to database!')


        expectedFiles = []
        for myFile in myTable.index:
            expectedFiles.append(myTable['Filename'][myFile])


        # check if dataset filenames in folderName are consistent with given md
        # sf -> subfolder (if nothing found in same directory, subfolder folderName is searched)
        if not os.path.isdir(os.path.join(csvDir,folderName)):
            sf = False
            warnings.warn('Cant find subfolder '+str(folderName)+'. Lets check if the files are in the same folder as the given csv file...')

            # checking as warning indicates
            if not all([True if i in os.listdir(csvDir) else False for i in expectedFiles]):
                notFound = [i if i not in os.listdir(csvDir) else 'Found' for i in expectedFiles]
                raise FileNotFoundError('Report on missing files: '+str(notFound))
        else:
            sf = True
        


        # check if headers of table are concistent with current md schema
        allFound = [True if i in list(myTable.columns) else False for i in self.listOfTemplateMDofDataset]
        if not allFound:
            raise Exception('Did not find all metadata columns needed for current md schema, please check!')


        
        # start reading in files:
        for row in myTable.index:
            currentListOfEntries = []
            currentFileName = myTable['Filename'][row]
            if sf:
                myDataset = pd.read_csv(os.path.join(csvDir,folderName,currentFileName),';')
            else:
                myDataset = pd.read_csv(currentFileName,';')
            for el in self.listOfTemplateMDofDataset:
                currentListOfEntries.append(myTable[el][row])
            print('nothing')
            self.addDataSet2ExistingFolder(folderName,currentListOfEntries,myDataset)

    # TODO everything
    def exportSchemaDF2CSV(self, folderPath, dfMD):
        '''
        purpose:    
        save csv file to disk
        create folders named in columns "Folder"
        create corresponding folder metadata files

        input:
        :param xxx:

        :return: 

        example:



        ===============================================================================================
    
        '''
        self.folderPath = folderPath
        self.dfMD = dfMD

    # TODO subfolder!
    def addFolder2ExistingDB(self,listOfEntries):
        '''
        purpose:
        if md schema exists, add row to table
        create folder md template from column folder
        add md schema to db for all folders

        input:
        :param listOfEntries: list of meta data information. 
        check mandatory fields via listOfTemplateMDofDB

        :return: none

        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        print(testDC.listOfTemplateMDofDB)
        >>['Folder','ID','Title','Description']

        # add a folder to your database
        myList2FillOut = ['newfolder', '1', 'This is a test', \
            'some kind of description text to describe the reason for the existence of this folder']
        testDC.addFolder2ExistingDB(listOfEntries=myList2FillOut)
   


        ===============================================================================================
       
        '''
        if len(listOfEntries) != len(self.listOfTemplateMDofDB):
            raise Exception('given list of entries incompatible with current metadata schema('\
                +str(len(listOfEntries))+' vs. '+str(len(self.listOfTemplateMDofDB))+')!')

        
        if listOfEntries[0] != listOfEntries[0].replace(" ",""):
            listOfEntries[0] = listOfEntries[0].replace(" ","")
            warnings.warn('Please be advised, no whitespaces in foldernames! \
            \nRemoving whitespaces before entering into database')

        with h5py.File(self.h5Filename,'a') as db:
            # check if folder exists already!
            listOfExistingFolders = list(db.keys())
            folderExists = bool(set([listOfEntries[0]]).intersection(set(listOfExistingFolders)))
            if not folderExists:
                db.create_group(listOfEntries[0])
                for index,run in enumerate(self.listOfTemplateMDofDB):
                    # for each folder 1 entry exists
                    if not db.attrs.__contains__(run): # if this is the first entry
                        myList = []
                    else: # otherwise just add to the list
                        myList = list(db.attrs.__getitem__(run))
                    myList.append(listOfEntries[index])
                    db.attrs[run] = myList
            else:
                raise Exception('This folder already exists!')

    # TODO add error of user catches
    # TODO test
    # TODO write self test
    # TODO test what happens if data is in the folder? if everythin is deleted, add sure flag
    def removeFolder(self,folderName: str):
        '''
        purpose:
        removes an existing folder from database.

        input:
        :param folderName: the name of the folder in the db (first entry in md schema)

        :return: none

        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname,'new')

        # add a folder to your database
        myList2FillOut = ['newfolder', '1', 'This is a test', \
            'some kind of description text to describe the reason for the existence of this folder']
        testDC.addFolder2ExistingDB(listOfEntries=myList2FillOut)

        testDC.getMDFromDB()

        testDC.removeFolder('newfolder')

        testDC.getMDFromDB()


        ===============================================================================================
        '''
        with h5py.File(self.h5Filename,"a") as db:
            db.__delitem__(folderName)
            foldInd = list(db.attrs['Folder']).index(folderName)
            for attr in db.attrs.keys():
                myList = list(db.attrs[attr])
                del myList[foldInd]
                db.attrs[attr] = myList

        print('folder and corresponding meta data removed')

    # TODO test
    # TODO subfolder! 
    # TODO check axis are realy attached to correct dataframes!
    def addDataSet2ExistingFolder(self,folderName,listOfDataEntries,datasetDF):
        '''
        purpose: 
        if md schema exists, add row to metadata table in folder
        add dataset to hdf5, reference to name of Dataset
        add metadata scheme of dataset to folder md schema
        NOTE that only 2D dataframes are tested to be stored in this DB!
        NOTE that category 'ID' needs to be unique in this Folder,
        otherwise returns error!

        input:
        :param folderName: name of an existing folder within hdf5 database
        :param listOfDataEntries: list of metadata information of current md schema
        :param datasetDF: a pandas dataframe with information about axis

        :return: 
        
        example:
        from supplychainmodelhelper import mds
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
        print(testDC.listOfTemplateMDofDataset)
        >>['Dataset','Filename','Format','ID','Title','Rows','Columns','Encoding']

        # add dataset to an existing folder
        myList2FillOut = ['distancematrix', 'distmatrix.csv', 'csv', '1', 'Distance matrix', \\
            str(len(list(myDF.index))), str(len(list(myDF.columns))), 'utf-8']
        testDC.addDataSet2ExistingFolder(folderName='newfolder', listOfDataEntries=myList2FillOut, datasetDF=myDF)



        ===============================================================================================
        
        '''
        self.listOfDataEntries = listOfDataEntries
        self.folderName = folderName 
        self.datasetDF = datasetDF
        if len(self.listOfDataEntries) != len(self.listOfTemplateMDofDataset):
            raise Exception('given list of entries incompatible with current metadata schema!')
        
        if listOfDataEntries[0] != listOfDataEntries[0].replace(" ",""):
            listOfDataEntries[0] = listOfDataEntries[0].replace(" ","")
            warnings.warn('Please be advised, no whitespaces in datasetnames! Removing whitespaces before entering into database')

        isThereAnObject = [True if i==object else False for i in list(datasetDF.dtypes)]
        if any(isThereAnObject):
            if isThereAnObject[0]:
                datasetDF.index = datasetDF[list(datasetDF.columns)[0]]
                del datasetDF[list(datasetDF.columns)[0]]
            else:
                raise Exception('currently only numbers are accepted in this database')

        # create dataset
        # add list of datasets with metadata to database
        # attach metadata of dataset to folder
        # listOfTemplateMDofDataset = ['Dataset'-0,'Filename'-1,'Format'-2,'ID'-3,'Title'-4,'Rows'-5,'Columns'-6,'Encoding'-7]
        with h5py.File(self.h5Filename,'a') as db:
            # check if folder exists
            listOfExistingFolders = list(db.keys())
            folderExists = bool(set([folderName]).intersection(set(listOfExistingFolders)))

            if folderExists:
                # adding dataset to hdf5 file
                nameOfDataSet = listOfDataEntries[0]
                # check if name of data set exists already in this folder
                listOfExistingDataSetsinFolder = list(db[folderName].keys())
                DataSetExists = bool(set([nameOfDataSet]).intersection(set(listOfExistingDataSetsinFolder)))
                #id checker
                if db[folderName].attrs.__contains__('ID'):
                    listOfExistingIDsinFolder = list(db[folderName].attrs['ID'])
                    idOfDataSet = listOfDataEntries[3]
                    idExists = bool(set([idOfDataSet]).intersection(set(listOfExistingIDsinFolder)))
                else:
                    idExists = False

                if idExists:
                    raise Exception('Please choose another ID!')

                # start entering data after checking if folder exists and dataset is new
                if not DataSetExists:
                    # store data set in db
                    myD = db[folderName].create_dataset(name=nameOfDataSet,data=datasetDF)
                    
                    # store md attached to dataset in db
                    for index,run in enumerate(self.listOfTemplateMDofDataset):
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
                        db[self.folderName].create_dataset("ScaleRowOfDataSet"+str(listOfDataEntries[3]), \
                            data=self.datasetDF.index.astype(int).values, dtype=dtIndex)
                    except TypeError:
                        dtIndex = h5py.string_dtype(encoding='utf-8')
                        db[self.folderName].create_dataset("ScaleRowOfDataSet"+str(listOfDataEntries[3]), \
                        data=self.datasetDF.index.values, dtype=dtIndex)
                    myD.dims[0].label = self.listOfTemplateMDofDataset[5]
                    myD.dims[0].attach_scale(db[folderName+'/ScaleRowOfDataSet'+str(listOfDataEntries[3])])

                    try:
                        dtCol = 'i'
                        db[self.folderName].create_dataset("ScaleColOfDataSet"+str(listOfDataEntries[3]), \
                            data=self.datasetDF.columns.astype(int).values, dtype=dtCol)
                    except TypeError:
                        # this only works for py3!
                        dtCol = h5py.string_dtype(encoding='utf-8')
                        db[self.folderName].create_dataset("ScaleColOfDataSet"+str(listOfDataEntries[3]), \
                            data=self.datasetDF.columns.values, dtype=dtCol)
                    # encoding list of strings to list of b-strings (py3 necessity)
                    myD.dims[1].label = self.listOfTemplateMDofDataset[6]
                    myD.dims[1].attach_scale(db[self.folderName+"/ScaleColOfDataSet"+str(listOfDataEntries[3])])
                    # listOfTemplateMDofDataset = ['Dataset'-0,'Filename'-1,'Format'-2,'ID'-3,'Title'-4,'Rows'-5,'Columns'-6,'Encoding'-7]
                else: 
                    raise Exception('Name of data set already exists in this particular folder, must be unique!')
            else: 
                raise Exception('This folder does NOT exist. Please create a folder by this name!')

    # TODO add error of user catches
    # TODO test
    # TODO write self test now
    def removeDatasetFromFolder(self,folderName,datasetName):
        '''
        purpose:
        removes an existing dataset in an existing folder from database.

        input:
        :param folderName: the name of the folder in the db
        :param datasetName: the name of the dataset in the folder 'folderName'

        :return: none

        example:
        from supplychainmodelhelper import mds
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
        print(testDC.listOfTemplateMDofDataset)
        >>['Dataset','Filename','Format','ID','Title','Rows','Columns','Encoding']

        # add dataset to an existing folder
        myList2FillOut = ['distancematrix', 'distmatrix.csv', 'csv', '1', 'Distance matrix', \\
            str(len(list(myDF.index))), str(len(list(myDF.columns))), 'utf-8']
        testDC.addDataSet2ExistingFolder(folderName='newfolder', listOfDataEntries=myList2FillOut, datasetDF=myDF)

        testDC.removeDatasetFromFolder('newfolder','distancematrix')


        ===============================================================================================
        '''

        with h5py.File(self.h5Filename,"a") as db:

            dsInd = list(db[folderName].attrs['Dataset']).index(datasetName)
            for index,run in enumerate(db[folderName].attrs.keys()):
                myList = list(db[folderName].attrs[run])
                del myList[dsInd]
                db[folderName].attrs[run] = myList

            del db[folderName + '/' + datasetName]
            #listOfMDNames = list()
        print('dataset removed')

    # TODO test
    def getDataFrameFromFolder(self,folderName,nameOfDataSet):
        '''
        
        purpose: retrieve dataset from hdf5 db as pandas data frame

        input:
        :param folderName: name of an existing folder within hdf5 database
        :param nameOfDataSet: the name of the dataset given in list of md schema
        (first element of this list)

        :return: the dataframe with axis(if exist)
        
        example:        
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve existing dataset back from database (created by addDataSet2ExistingFolder)
         myDatasetFromhdf5DB = testDC.getDataFrameFromFolder(folderName='newfolder',nameOfDataSet='distancematrix')
    


        ===============================================================================================    
        
       
        '''
        self.folderName = folderName
        self.nameOfDataSet = nameOfDataSet
              
        with h5py.File(self.h5Filename,'r') as db:
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

    # TODO test
    def getMDFromDataSet(self,folderName,nameOfDataSet):
        '''
        
        purpose: retrieve metadata from dataset in hdf5 db

        input:
        :param folderName: name of an existing folder within hdf5 database
        :param nameOfDataSet: the name of the dataset given in list of md schema
        (first element of this list)

        :return: a dataframe(2 column table) of information about an existing dataset
        with headers: MD Names, Content
        
        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve existing dataset back from database (created by addDataSet2ExistingFolder)
        print(testDC.getMDFromDataSet(folderName='newfolder',nameOfDataSet='distancematrix'))        



        ===============================================================================================
        
        '''
        self.folderName = folderName
        self.nameOfDataSet = nameOfDataSet
        listOfMDNames = []
        listOfMDContents = []
        
        with h5py.File(self.h5Filename,'r') as db:
            try:
                for x in db[folderName+'/'+nameOfDataSet].attrs.__iter__():
                    listOfMDNames.append(x)
                    listOfMDContents.append(db[folderName+'/'+nameOfDataSet].attrs.__getitem__(x))
            except KeyError:
                raise Exception('data set with this name is not stored here!')
        return pd.DataFrame(data={'MD Names':listOfMDNames,'Content':listOfMDContents})

    # TODO get like DB otherwise IT WONT WORK!
    def getMDFromFolder(self,folderName):
        '''
        purpose:        
        retrieve metadata from folder, information about the folder in question
        and which information they contain

        input:
        :param folderName: name of an existing folder within hdf5 database

        :return:  a dataframe(2 column table) of information about an existing dataset
        with headers: MD Names, Content wit list of all datasets
        
        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve existing folder back from database (created by addDataSet2ExistingFolder)
        print(testDC.getMDFromFolder(folderName='newfolder'))



        ===============================================================================================
        '''
        self.folderName = folderName
        listOfMDNames = []
        listOfMDContents = []
        
        with h5py.File(self.h5Filename,'r') as db:
            try:
                for x in db[folderName].attrs.__iter__():
                    listOfMDNames.append(x)
                    listOfMDContents.append(db[folderName].attrs.__getitem__(x))
            except KeyError:
                raise Exception('foldername with this name is not stored here!')
        return pd.DataFrame(data={'MD Names':listOfMDNames,'Content':listOfMDContents})
    
    # TODO test with different content and customized metadata schemas
    def getMDFromDB(self):
        ''' 
        purpose:
        retrieve metadata from db, information about folders in this database and which information they contain
        returned as pandas dataframe

        input: no parameters needed, as each instance deals with just one databas

        :return: a dataframe (multi-column table) of information about an existing dataset
        with headers based on current md schema (basic schema headers: Description, Folder, ID, Title,)
        
        example:
        from supplychainmodelhelper import mds

        myfname = './testDCnew.hdf5'
        testDC = mds.Datacube(myfname)

         # retrieve md info about database (created by addDataSet2ExistingFolder)        
        print(testDC.getMDFromDB())



        ===============================================================================================
        '''
        try:
            with h5py.File(self.h5Filename,'r') as db:
                myKeys = [key for key in db.attrs.keys()]
                myVals = [val for val in db.attrs.values()]
        except KeyError:
            raise Exception('data set with this name is not stored here!')
        
        myDF = pd.DataFrame(columns=myKeys)
        for i,x in enumerate(myVals):
            myDF[myKeys[i]] = list(myVals[i])
        return myDF
