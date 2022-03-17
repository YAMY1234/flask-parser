import pandas as pd
import json
import re
import os

'../source_file/analysis.table'

explist = []
leftlist = []
rightlist = []
index=0
S={}

def read_data():
    path=os.getcwd()+'/source_file/analysis.table'
    try:
        table = pd.read_table(path)
    except:
        table=pd.read_table(path,encoding='gbk')
    df=pd.DataFrame(table)
    df=df.iloc[:,3]
    global explist
    global leftlist
    global rightlist
    explist = []
    leftlist = []
    rightlist = []
    for i in range(len(df))[::-1]:
        if re.search('reduce',df[i])!=None:
            tmp=re.findall('(?<=\().+(?= ,)',df[i])
            explist.append(tmp)

    for item in explist:
        item=item[0]
        itemarray=item.split('->')
        left=itemarray[0]
        right=itemarray[1]
        right=right.split(' ')
        leftlist.append(left)
        rightlist.append(right)

# print(leftlist)
# print(rightlist)

def makeNode(name):
    node=dict()
    node['name']=name
    if node['name']=='$':
        node['NodeType']='T'
    else:
        node['NodeType'] = 'NT'
    node['children']=[]
    return node

def MakeNodeList(right):
    NodeList=[]
    for i in right:
        NodeList.append(makeNode(i))
    return NodeList


def add_node(node,left,right):
    global leftlist
    global rightlist
    global index
    if node['name']==left:
        newNodeList=MakeNodeList(right)
        for item in newNodeList:
            node['children'].append(item)
        index+=1
        cnum=len(node['children'])
        for i in range(cnum):
            if index >= len(leftlist):
                return
            left = leftlist[index]
            right = rightlist[index]
            add_node(node['children'][cnum-i-1],left,right)


def shapeTree():
    global index
    global leftlist
    global rightlist
    global S
    S = makeNode('start')
    index=0
    left = leftlist[0]
    right = rightlist[0]
    add_node(S, left, right)

def getS():
    import time
    read_data()
    shapeTree()
    global S
    return S
# print(S)