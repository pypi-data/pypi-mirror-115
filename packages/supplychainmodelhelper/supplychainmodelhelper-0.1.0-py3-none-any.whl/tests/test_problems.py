# %%

import os
import h5py
import csv
import pandas as pd # 0.25.2
import sys
sys.path.append('../')
#from supplychainmodulator.datahandling import importDataFromFolder
#from supplychainmodulator.datahandling import decBS, decBSList
from supplychainmodulator.graphoperations \
    import createGraph, \
        getListOfNodeIDs, \
            addAttr2ExistingNodes,\
                getNodeIDswAttr,\
                    proxyModel,\
                        convertTup2LoT,\
                            convertLoT2NTs,\
                                getExistingAttrs,\
                                    getEdgeID,\
                                        addAttr2Edges,\
                                            getEdgesAttr,\
                                                getEdgeIDswAttr,\
                                                    furnessModel,\
                                                        minOptFlowForBeta,\
                                                            hymanModel,\
                                                                calcPotTransportDistances,\
                                                                    getAllCombinations
                                                    




test = 'mytest'
#btest = b'mytest'

prod = ['milk','beer','schnaps']
act = ['producer','consumer','warehouse','store']
loc = ['BER','SXF','TXL']

T = createGraph(act,loc,prod)

#print(T.nodes)

#print(getListOfNodeIDs(T,['producer','store'],['milsk','bseer'],['BER','SX']))
#print(getListOfNodeIDs(T,['producer'],['milk'],['BER']))
myList = getListOfNodeIDs(T,\
    products=['milk','schnaps'],\
        actors=['producer'],\
            locations=['BER','SXF'])
print('my NodeIDs:\n')
print(getListOfNodeIDs(T,products=['milk','schnaps'],actors=['producer'],locations=['BER','SXF']))
didItWork = addAttr2ExistingNodes(T,myList,'test',list(range(len(myList))))
print('\nDid It Work?: '+str(didItWork))
print('\nAll infos:')
print(T.nodes(data=True))
print('\n get me just this:')
a = getNodeIDswAttr(T,'test',myList)
print(a)

print('\n now get me the unpacked version:')
b,c = convertLoT2NTs(a)
print(b,c)

print('\nback to original')
a1 = convertTup2LoT(b,c)
print(a1)

print('test the conversion if just a list is given')
try:
    b1,c1 = convertLoT2NTs(b)
except TypeError:
    print('it is good that this doesnt work')



nl = [1,2,3]
ip = 10
pn = 100
print('\n AND now the model w/o node ids')
print(proxyModel(ip,nl,pn))

print('\n AND now the model w node ids')
nid = [0,1,2]
wid = [10.1,20.3,17.33]
nl2 = convertTup2LoT(nid,nl)
print(nl2)
print(proxyModel(ip,nl2,pn))



print('\ngive me a list of edgeIDs:')
e = getEdgeID(T,nid,nl)
print(e)

print('\nLets try the proxy model on edges:')
e = getEdgeID(T,nid,nl)
diw = addAttr2Edges(T,e,wid,'newstuff')
print('did it work:'+str(diw))
el = getEdgeIDswAttr(T,'newstuff',e)
print(el)
print(proxyModel(pn,el,ip))

print('\ngive me a list of edgeIDs with nonexisting nodes:')
try:
    getEdgeID(T,nid,wid)
except Exception:
    print('naughty boy!')
print(e)


print('\nAdding this list of edge ids to graph')
try:
    addAttr2Edges(T,e,[])
except Exception:
    print('didnt work! good')

print('next we add some edges to the graph')
try:
    w = addAttr2Edges(T,e,wid)
    if w:
        print('it worked!')
except Exception:
    print('didnt work! Not good')

print('next we add some edges with a different attribute to the graph')
try:
    w = addAttr2Edges(T,e,list(range(len(e))),'teste')
    if w:
        print('it worked!')
except Exception:
    print('didnt work! Not good')


print('\nLets see what kind of attributes you did think of:')
print('default:')
print(getExistingAttrs(T))
print('nodes:')
print(getExistingAttrs(T,'n'))
print('edges:')
ae = getExistingAttrs(T,'e')
print(ae)
print('nonsense:')
print(getExistingAttrs(T,2))

print('\nlets get edges attributes: default')
print(getEdgesAttr(T))

print('\nlets get edges attributes: '+ae[0])
print(getEdgesAttr(T,attr=ae[0]))

print('\nlets get edges attributes: '+ae[1])
print(getEdgesAttr(T,attr=ae[1]))


print('\n lets get the whole deal')
print(getEdgeIDswAttr(T))
ma,mb,mc = convertLoT2NTs(getEdgeIDswAttr(T))
print(ma)
print(mb)
print(mc)

print('\nTest if convert tuples to LoT works:')
print(convertTup2LoT((1,2),(2,3)))
mrt = convertTup2LoT([(1,2),(3,4)],(2,3))
print(mrt)
print(proxyModel(1,mrt,2))

print('\nAnd now to test this gravity model everyone is speaking of:')
lop = getListOfNodeIDs(T,actors=['producer'],products=['milk'])
loc = getListOfNodeIDs(T,actors=['consumer'],products=['milk'])
didItWork = addAttr2ExistingNodes(T,lop, 'output', [10,20,30])
if didItWork: print('attribute added to graph')
didItWork = addAttr2ExistingNodes(T,loc, 'input', [5,10,45])
if didItWork: print('attribute added to graph')
t1 = [x for x in lop for _ in loc]
t2 = [y for _ in lop for y in loc]
myoutin = getEdgeID(T,t1,t2)
didItWork = addAttr2Edges(T,myoutin, [1,2,50,2,1,49,50,49,1],attr='distance')
if didItWork: print('attribute added to graph')
print('is this right?')
#myoutin.append((12,12))
res = getEdgesAttr(T,attr='distance',listOfEdgeIDs=myoutin)
print(res)

print('\ndoes all combinations work?')
vv1,vv2 = getAllCombinations(prod,act,order='2nd')
print(vv1)
print(vv2)

print('\nTest if nodes are in graph')
try:
    print(getNodeIDswAttr(T,'test'))
except Exception:
    print('works fine!')
#thisFlow=furnessModel(T,lop,loc,0.1,'distance','exp')
#print(thisFlow)
#print('lets test this sucker:')
#import numpy as np
#print(np.sum(thisFlow))
#print(np.sum(thisFlow,0))
#print(np.sum(thisFlow,1))
#print('\nplease get me beta_opt:')
#betaopt=minOptFlowForBeta(T, lop, loc, 4, 'distance', 'exp')
#print(betaopt)
#print('\nwhat now hyman:')
#ff=hymanModel(T, lop, loc, 30.)
#print(ff)
#print('\ntry calc dists:')
#dd = calcPotTransportDistances(T, lop, loc, 5)

# print('list of senders:'+str(lop))
# print('list of reveivers:'+str(loc))
# dm = pd.DataFrame({'BER':[1,2,50],'SXF':[2,1,49],'TXL':[50,49,1]},index=['BER','SXF','TXL'])
# print('distance matrix:')
# print(dm)
# flow = gravityModel(T,lop,loc,0.1,dm,'exp')
# print('What happened?')
# print(flow)
#tbl = [b'tegd',b'tegdg',b'FDdfdf']

#print(test,btest,decBS(test),decBS(btest))
#print(tl,tbl,decBSList(tl),decBSList(tbl))

#print(combineActorBrand(actor=test,brand=tl))
#fileInputPath = "../data/metadata/"
#fileInMetadataName = "folderMD.csv"
#fileOutputName = "test.hdf5"



#ymy = importDataFromFolder(fileInputPath,fileInMetadataName,fileOutputName)


# %%
