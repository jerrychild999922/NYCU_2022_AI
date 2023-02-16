import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'
# Begin your code (Part 4)
"""
My main idea is to create a class that record every point's state 
and which point they can go...

(line 27 to 39) is the construction of my class 
explanation the same as part 1
* I add a h to represent point's heuristic

(line 42 to 73) is how I record point's information to class
explanation the same as part 1
* add I use h1,h2,h3 to save heuristic.csv

(line 74 to 77 ) is to get the start point and put it in q=[]

(line 78 to 113 ) is the main astar function
actually, it is similar to ucs, however i use .d to judge which edge go first
and now, i use .h to judge

(line 114 to 130 ) is to find the result return 
explanation the same as part 1
"""
class graph:
    def __init__(self,num,to,dis):
        self.d=0
        self.h=0
        self.num=num
        self.color=0
        self.distance=[]
        self.pre=-1
        self.list=[]
        self.list.append(to)
        self.distance.append(dis)
    def add(self,to,dis):
        self.list.append(to)
        self.distance.append(dis)

def astar(start, end):
    a=[]
    b=[]
    j=0
    tem=0
    count=0
    file=open(edgeFile)
    for i in file.readlines():
        if(j>0):
            ii=i.split(',')
            if(tem==int(ii[0])):
                a[len(a)-1].add(int(ii[1]),float(ii[2]))
            else:
                a.append(graph(int(ii[0]),int(ii[1]),float(ii[2])))
                b.append(int(ii[0]))
                tem=int(ii[0])
        j=j+1
    file.close()
    j=0
    h1={}
    h2={}
    h3={}
    file=open(heuristicFile)
    for i in file.readlines():
        if(j>0):
            ii=i.split('\r')
            iii=ii[0].split(',')

            h1.update({int(iii[0]):float(iii[1])})
            h2.update({int(iii[0]):float(iii[2])})
            h3.update({int(iii[0]):float(iii[3])})
        j=j+1
    file.close()
    s=0
    for i in range(len(a)):
        if(a[i].num==start):
            s=i
    q=[]
    q.append(a[s])
    while not(len(q)==0):
        
        m=0
        min=10000000
        for i in range(len(q)) :
            if(q[i].h<min):
                min=q[i].h
                m=i
    
        u=q[m]
        q.pop(m)
        u.color=1
        count=count+1
        if(u.num==end):
            break
        for i in range(len(u.list)):
            if u.list[i] in b :
                l=b.index(u.list[i])
                if(a[l].color==0):
                    if a[l] in q:
                        if a[l].d>u.d+u.distance[i]:
                            a[l].d=u.d+u.distance[i]
                            a[l].h=u.d+u.distance[i]+h1[a[l].num]
                            a[l].pre=u.num
                    else:
                        q.append(a[l])
                        a[l].d=u.d+u.distance[i]
                        a[l].h=u.d+u.distance[i]+h1[a[l].num]
                        a[l].pre=u.num
            else :
                a.append(graph(u.list[i],0,0))
                b.append(u.list[i])
                a[len(a)-1].d=u.d+u.distance[i]
                a[len(a)-1].pre=u.num
    path=[]
    s=0
    for i in range(len(a)):
        if(a[i].num==end):
            s=i
    dis=a[s].d
    path.append(a[s].num)
    while(1):
        k=a[s].pre
        path.append(k)
        if(k==start):
            break
        else:
            s=b.index(k)
    return path , dis , count
#raise NotImplementedError("To be implemented")
# End your code (Part 4)

'''
if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
'''