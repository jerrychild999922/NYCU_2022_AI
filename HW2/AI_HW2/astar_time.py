import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

# Begin your code (Part 6)
'''
Because my astar_time is similar to astar, I just mention the diffence
First:  I add a state .t represent the time spent from start to the point
        and time[] it save the speed limit
Second: I use .t to judge which point pop first instead of .d, which means
        I use time to become my heuristic function






'''
class graph:
    def __init__(self,num,to,dis,time):
        self.t=0
        self.d=0
        self.h=0
        self.num=num
        self.color=0
        self.distance=[]
        self.time=[]
        self.pre=-1
        self.list=[]
        self.list.append(to)
        self.distance.append(dis)
        self.time.append(time)
    def add(self,to,dis,time):
        self.list.append(to)
        self.distance.append(dis)
        self.time.append(time)

def astar_time(start, end):
    a=[]
    b=[]
    j=0
    tem=0
    file=open(edgeFile)
    for i in file.readlines():
        if(j>0):
            ii=i.split(',')
            if(tem==int(ii[0])):
                a[len(a)-1].add(int(ii[1]),float(ii[2]),float(ii[3]))
            else:
                a.append(graph(int(ii[0]),int(ii[1]),float(ii[2]),float(ii[3])))
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

    count=0
    q=[]
    q.append(a[s])
    while not(len(q)==0):
        m=0
        min=10000000
        for i in range(len(q)) :
            if(q[i].t<min):
                min=q[i].t
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
                        if a[l].t>u.t+(u.distance[i]/(u.time[i]*1000/3600)):
                            a[l].d=u.d+u.distance[i]
                            a[l].h=u.d+u.distance[i]+h1[a[l].num]
                            a[l].t=u.t+(u.distance[i]/(u.time[i]*1000/3600))
                            a[l].pre=u.num
                    else:
                        q.append(a[l])
                        a[l].d=u.d+u.distance[i]
                        a[l].h=u.d+u.distance[i]+h1[a[l].num]
                        a[l].t=u.t+(u.distance[i]/(u.time[i]*1000/3600))
                        a[l].pre=u.num         
        
    path=[]
    s=0
    for i in range(len(a)):
        if(a[i].num==end):
            s=i
        
    dis=a[s].t
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
    # End your code (Part 6)

'''
if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
'''