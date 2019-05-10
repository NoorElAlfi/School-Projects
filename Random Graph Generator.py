import random
#Queue Class
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
#vertex class    
class Vertex:
    def __init__(self, node):
        self.Key = node
        self.neighbour = {}
    #to string methof
    def __str__(self):
        return str(self.Key) + ' adjacent: ' + str([x.Key for x in self.neighbour])
    #add edge
    def addNeighbor(self, neighbor, weight=0):
        self.neighbour[neighbor] = weight
    #Get all edges of current vertex
    def getConnections(self):
        return self.neighbour.keys()  
    #Get key of vertex
    def getKey(self):
        return self.Key
    #Get weight of current vertex and given adjacent edge
    def getWeight(self, neighbor):
        return self.neighbour[neighbor]
#graph class
class Graph:
    #randomizes graph if value given else creates empty graph
    def __init__(self, n):
        self.vertices = {}
        self.num_vertices = 0
        if n != 0:    
            for i in range(n):
                self.addVertex(i)
            self.addEdge(0,(random.randint(1,n)),(random.randint(10,100)))
            for i in range(2, n):
                x = random.randint(1,i-1)
                S = [] 
                for j in range(x):
                    S.append(random.randint(1,i-1))
                for s in S:
                    w = random.randint(10,100)
                    self.addEdge(i,s,w)

    # allows graph to be iterable
    def __iter__(self):
        return iter(self.vertices.values())
    
    #Adds vertex to graph 
    def addVertex(self, node):
        if node not in self.vertices:
            self.num_vertices = self.num_vertices + 1
        newVertex = Vertex(node)
        self.vertices[node] = newVertex
        return newVertex
    #gets vertex given as argument
    def getVertex(self, n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None
    #adds edge between given arguments
    def addEdge(self, frm, to, cost = 0):
        if frm not in self.vertices:#checks if vertex exists else creates vertex
            self.addVertex(frm)
        if to not in self.vertices:
            self.addVertex(to)

        self.vertices[frm].addNeighbor(self.vertices[to], cost)
        self.vertices[to].addNeighbor(self.vertices[frm], cost)
    #gets verticies
    def getVertices(self):
        return self.vertices.keys()
    #Puts all edges of graph in list
    def getEdges(self):
        edges = []
        for v in self:
            for i in v.getConnections():
                edge = (v.getKey(), i.getKey(), v.getWeight(i))
                if edge not in edges:
                    edges.append(edge)
        return edges
    #Breadth first search using queue
    def BFS(self):
        total = 0
        sVertex = random.choice(list(g.vertices.keys()))
        q = Queue()
        q.enqueue(sVertex)
        visited = []
        while not(q.isEmpty()):
            x = q.dequeue()
            if(x not in visited):
                visited.append(x)
            for y in self.vertices[x].neighbour:
                if(not(y.getKey() in visited)):
                    q.enqueue(y.getKey())
                    visited.append(y.getKey())
                    total += self.vertices[x].getWeight(y)
        return total
    #Prims algorithm
    def mst_prim(self):
        #creates minimum spanning tree
        mst = Graph(0)
        total = 0
        if not self:
            return mst
        nearestNeighbour = {}
        smallestDistance = {}
        unvisited = set(self)
     
        u = next(iter(self)) 
        mst.addVertex(u.getKey()) 
        unvisited.remove(u)
        for n in u.getConnections():
            if n is u:
                continue
            nearestNeighbour[n] = mst.getVertex(u.getKey())
            smallestDistance[n] = u.getWeight(n)
     
        while (smallestDistance):
            outsideMst = min(smallestDistance, key=smallestDistance.get)
            insideMst = nearestNeighbour[outsideMst]
            mst.addVertex(outsideMst.getKey())
            mst.addEdge(outsideMst.getKey(), insideMst.getKey(),
                         smallestDistance[outsideMst])
            mst.addEdge(insideMst.getKey(), outsideMst.getKey(),
                         smallestDistance[outsideMst])
            unvisited.remove(outsideMst)
            del smallestDistance[outsideMst]
            del nearestNeighbour[outsideMst]
            for n in outsideMst.getConnections():
                if n in unvisited:
                    if n not in smallestDistance:
                        smallestDistance[n] = outsideMst.getWeight(n)
                        nearestNeighbour[n] = mst.getVertex(outsideMst.getKey())
                    else:
                        if smallestDistance[n] > outsideMst.getWeight(n):
                            smallestDistance[n] = outsideMst.getWeight(n)
                            nearestNeighbour[n] = mst.getVertex(outsideMst.getKey())
        #calculates total of edges in MST
        visited = []
        for v in mst:
            if v not in visited:
                visited.append(v)
            for i in v.getConnections():
                if i not in visited:
                    total += v.getWeight(i)
                    visited.append(i)
        return total
    #union-find find method    
    def findk(self, C, u):
        while(C[u] != u):
            u = C[u]
        return u
    #union-find union method
    def unionK(self, C, R, u, v):
        u, v = self.findk(C, u), self.findk(C, v)
        if R[u] > R[v]:
            C[v] = u
        else:
            C[u] = v
        if R[u] == R[v]:
            R[v] += 1
    #kruskal's algorithm
    def kruskal_mst(self):
        total = 0
        F = self.getEdges()
        E = sorted(F, key = lambda i:i[2])
        T = set()
        C = {u.getKey():u.getKey() for u in self}
        R = {u.getKey():0 for u in self}
        for u,v,w in E:
            if self.findk(C, u) != self.findk(C, v):
                T.add((u, v))
                self.unionK(C, R, u, v)
                total += w
        return total         
#compare prims and BFS
def compareAlgos(k):
    avgs = []
    for n in range(20,80,20):
        kAvg = []
        for i in range(0,k+1):
            graph = Graph(n)
            B = graph.BFS()
            P = graph.mst_prim()
            diff = (B - P)/10
            kAvg.append(diff)
        diff = sum(kAvg) / len(kAvg)
        avgs.append(diff)
        print("n = %d" % n)
        print("Average = %f" % diff)
    return avgs
        
            
        
    
    
    
if __name__ == '__main__':
    g = Graph(5) 
    for x in g.vertices:
        print(g.vertices[x])
    for v in g:
        for w in v.getConnections():
            vid = v.getKey()
            wid = w.getKey()
            print ("( %s , %s, %3d)"  % ( vid, wid, v.getWeight(w)))    
    print(g.BFS())
    print(g.mst_prim())
    print(g.kruskal_mst())
    compareAlgos(3)