f=open("info5.txt","r",encoding='utf-8')
f.readline()
data=[]
for line in f:
    print (line)
    data.append(line)
leftlist=[]
rightlist=[]
produtionList=[]
for item in data:
    item.split("::=")
    left=item[0]
    right=item[1]
    leftlist.append(left)
    right=right.split("|")
    for jtem in right:
        jtem_split=jtem.split()
