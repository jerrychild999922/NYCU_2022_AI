import csv
import queue
edgeFile = 'edges.csv'

# Begin your code (Part 1)
"""
My main idea is to create a class that record every point's state 
and which point they can go...

(line 44 to 56) is the construction of my class 
d          represent the distance it have passed from start point to this point
num        represent the point address
color      represent whether it have been passed
pre        represent the previous point 
list[]     represent all the points this point can go 
distance[] represent the distance from this points to next point respectively

(line 59 to 76) is how I record point's information to class
a[] is a array to save all the class
b[] is just a array to save the point address 
    in order to find the location of a point in a[]
j   is avoid getting the first line
tem is avoid creating the same point
count is to count how many point i visited

(line 79 to 82 ) is to get the start point and put it in quene

(line 84 to 103 ) is the main bfs function
step 1: I get the point(oldest) and put all points 
        which it(oldest) can go to in quene and update their state
step 2: repeat step 1 until the end point be get from quene
* need to pay attention to the point not in 
  a[](these points mean can't go to another points ) need add them to a[]

(line 105 to 122 ) is to find the result return 
step 1: I find the end point and use it.pre to get its previous point 
        until the start point gotten
step 2: record all the point in step 2 in path[]
step 3: dis is just the end point.d
step 4: count can be return directly

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

def bfs(start, end):
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

    
    s=0
    for i in range(len(a)):
        if(a[i].num==start):
            s=i
            
    q = queue.Queue()
    q.put(a[s])
    while not(q.empty()):
        count=count+1
        u=q.get()
        if(u.num==end):
            break
        for i in range(len(u.list)):
            if u.list[i] in b :
                l=b.index(u.list[i])
                if(a[l].color==0):
                    q.put(a[l])
                    a[l].d=u.d+u.distance[i]
                    a[l].pre=u.num
                    a[l].color=1
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
# End your code (Part 1)

if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')