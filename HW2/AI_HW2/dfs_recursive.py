import csv
import sys
sys.setrecursionlimit(100000000)

edgeFile = 'edges.csv'

# Begin your code (Part 2)
"""
My main idea is to create a class that record every point's state 
and which point they can go...

(line 31 to 43) is the construction of my class 
explanation the same as part 1

(line 46 to 61) is how I record point's information to class
explanation the same as part 1
*count become c[] because i want to bring it to recusive function

(line 79 to 87 ) is to get the start point and put it in function

(line 63 to 77 ) is the main dfs function
step 1: I get all points the start point can go to and do recursive 
        so it will find point and update the point's state until the leaf
        (which means it will go the road until it can't get to any new point)
* I dont set terminal condition because too complicated 

(line 89 to 106 ) is to find the result return 
explanation the same as part 1
"""

class graph:
    def __init__(self,num,to,dis):
        self.d=0
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

def dfs(start, end):
    a=[]
    b=[]
    j=0
    tem=0
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

    def dfss(p,a,b,c):
        
        c[0]=c[0]+1
        for i in range(len(p.list)):
            if p.list[i] in b :
                l=b.index(p.list[i])
                if(a[l].color==0):
                    a[l].d=p.d+p.distance[i]
                    a[l].pre=p.num
                    a[l].color=1
                    dfss(a[l],a,b,c)
            else:
                a.append(graph(p.list[i],0,0))
                a[len(a)-1].d=p.d+p.distance[i]
                a[len(a)-1].color=1

    s=0
    for i in range(len(a)):
        if(a[i].num==start):
            s=i

    c=[]
    c.append(0)
    a[s].color=1
    dfss(a[s],a,b,c)

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
            
    return path , dis , c[0]

#raise NotImplementedError("To be implemented")
# End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
