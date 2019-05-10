# -*- coding: utf-8 -*-
"""
Noor ElAlfi
20077198
Assignment 3
"""
import heapq
import glob
import os

'''
This class represents a node of the AVL tree
'''
class TreeNode(object): 
    def __init__(self, key, val): 
        self.key = key
        self.val = val 
        self.left = None
        self.right = None
        self.height = 1
  
'''
This class represents the AVL tree
'''
class AVLTreeMap(object): 
    '''
    This method searches for a given key in the tree and returns a list of all the nodes its passed
    '''
    def searchPath(self, root, key, path = []):
        if not root:
            return []
        if key < root.key:
            if root.left is None:
                return (str(key) + " Not Found.")
            path.append(root.key)
            return self.searchPath(root.left, key)
        elif key > root.key:
            if root.right is None:
                return (str(key) + " Not Found.")
            path.append(root.key)
            return self.searchPath(root.right, key)
        else:
            path.append(root.key)
            print("Found", key)
            return path
    '''
    This method searches for a given key and returns that value
    '''
    def get(self, root, key):
        if key < root.key:
            if root.left is None:
                return (str(key) + " Not Found.")
            return self.get(root.left, key)
        elif key > root.key:
            if root.right is None:
                return (str(key) + " Not Found.")
            return self.get(root.right, key)
        else:
            return root.key
    '''
    This method inserts a new node into the tree
    '''
    def put(self, root, key, val):       
        if not root: 
            return TreeNode(key, val) 
        elif key == root.key:
            root.val = val
        elif key < root.key: 
            root.left = self.put(root.left, key, val) 
        else: 
            root.right = self.put(root.right, key, val) 

        root.height = 1 + max(self.getHeight(root.left), 
                           self.getHeight(root.right)) 
        balance = self.getBalance(root) 
        # Case 1 - Left Left       
        if balance > 1 and key < root.left.key: 
            return self.rightRotate(root) 
        # Case 2 - Right Right 
        if balance < -1 and key > root.right.key: 
            return self.leftRotate(root) 
        # Case 3 - Left Right 
        if balance > 1 and key > root.left.key: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
        # Case 4 - Right Left 
        if balance < -1 and key < root.right.key: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
        return root 
    '''
    This method adjusts the AVL tree in certain case imbalance
    '''
    def leftRotate(self, z):   
        y = z.right 
        T2 = y.left   
        y.left = z 
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left), 
                         self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                         self.getHeight(y.right))   
        return y 
    '''
    This method adjusts the AVL tree in certain case imbalance
    '''
    def rightRotate(self, z):   
        y = z.left 
        T3 = y.right   
        y.right = z 
        z.left = T3   
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right))   
        return y 
    '''
    This method gets height of node
    '''
    def getHeight(self, root): 
        if not root: 
            return 0  
        return root.height 
    '''
    This method gets balance factor of node
    '''
    def getBalance(self, root): 
        if not root: 
            return 0  
        return self.getHeight(root.left) - self.getHeight(root.right) 
'''
This class represents the web page index which contains the webpage and an AVL tree of the webpage
'''
class WebPageIndex(object):
    def __init__(self, filename):
        self.filename = filename.lower()
        self.AVL = AVLTreeMap()
        self.node = self.fileToAVL(filename)  
    
    '''
    This method takes a web page and puts it in an AVL tree
    '''
    def fileToAVL(self, filename):
        fp = open(self.filename, "r")
        lis = []
        tree = AVLTreeMap()
        root = None
        for line in fp:
            lis.append(line.lower())
            lis = lis[0].split(" ")
            letters = "abcdefghijklmnopqrstuvwxyz"
            for i in lis:
                i = i.lower()
                newString = ""
                for char in i:
                    if char in letters:
                        newString += char
                i = newString
                root = tree.put(root, i, self.getIndex(i)) #insert node to tree
            lis = []
        fp.close()
        return root
    '''
    This method finds the amount of times a given word is found in the webpage
    '''
    def getCount(self,s):
        count = 0
        fp = open(self.filename, "r")
        lis = []
        for line in fp:
            lis.append(line.lower())
            lis = lis[0].split(" ")
            letters = "abcdefghijklmnopqrstuvwxyz"
            for i in lis:
                i = i.lower()
                newString = ""
                for char in i:
                    if char in letters:
                        newString += char
                i = newString
                if (i == s):
                    count += 1
            lis = []
        fp.close()
        return count
    '''
    This method finds the indicies in which the given word is found in the webpage(return list of indicies)          
    '''          
    def getIndex(self,s):
        index = []
        count = 0
        fp = open(self.filename, "r")
        lis = []
        for line in fp:
            lis.append(line.lower())
            lis = lis[0].split(" ")
            letters = "abcdefghijklmnopqrstuvwxyz"
            for i in lis:
                i = i.lower()
                newString = ""
                for char in i:
                    if char in letters:
                        newString += char
                i = newString
                if (i == s):
                    index.append(count)
            count += 1
            lis = []
        fp.close()
        return index 
'''
This class represents a web page priority queue based on the priority of webPage indexes(which is calculated by finding the amount of times the words in query appear in the webpage)
'''
class WebpagePriorityQueue(object):
    def __init__(self, WPI, query):
        self.queue = []
        self.query = query
        self.WPI = WPI
        self.enQueue(self.findPriority(WPI, query))
    '''
    This method creates the queue based on a list of web page instances
    '''
    def enQueue(self, pLis):
        for i in pLis:
            heapq.heappush(self.queue, i)
        heapq._heapify_max (self.queue)
        return self.queue
    '''
    This method finds the priority of  webpages and places it in an web page instance (returns list of all WPI) 
    '''
    def findPriority(self, WPI, query):
        query = query.split(" ")
        pLis = []
        for WP in self.WPI:
            priority = 0
            for i in query: 
                priority += WP.getCount(i)
            t = WebPageInstance (priority, WP)
            pLis.append(t)
        return pLis
    '''
    This method finds peek of priority queue
    '''
    def peek(self):
        return self.queue[0]
    
    '''
    This method removes top of queue and returns it
    '''
    def poll(self):
        rslt = self.queue.pop(0)
        heapq._heapify_max (self.queue)
        return rslt
    '''
    This method checks web page with new query 
    '''
    def reheap(self, nQuery):
        if self.query == nQuery:
            return 
        else:
            self.queue = []
            for i in self.WPI:
                priority = self.findPriority(i, nQuery)
                heapq.heappush(self.queue, priority)
            heapq._heapify_max (self.queue)

'''
This class represents the WPI which contains the priority of web page and the webpage this allows for type comparison when the WPI is being added to the priority queue
'''
class WebPageInstance(object):
    def __init__ (self, priority, page):
        self.priority = priority
        self.page = page
     #Less than   
    def __lt__ (self, other):
        if self.priority < other.priority:
            return True
        else:
            return False
    #Less than or equal   
    def __le__ (self, other):
        if self.priority <= other.priority:
            return True
        else:
            return False
    #Greater than    
    def __gt__ (self, other):
        if self.priority > other.priority:
            return True
        else:
            return False
    #Greater than or equal    
    def __ge__ (self, other):
        if self.priority <= other.priority:
            return True
        else:
            return False          
'''
This class represents the process Queries which takes a directory and a queries file and processes them
'''
class processQueries(object):
    def __init__(self, files, queries,USL):
        self.files = files
        self.queries = queries
        self.USL = USL
        queryLis = self.getQueries(queries)
        wLis = self.getWPI(files)
        pQ = self.mkQueue(queryLis, wLis)
        self.processQ(pQ, queryLis)
    '''
    This method gets Web page index from directory
    '''
    def getWPI(self, filePath):
        wLis = []
        fp = glob.glob (filePath)
        for file in fp:
            wLis.append(WebPageIndex(file))
        return wLis
    '''
    This method gets list of queries from text file
    '''
    def getQueries(self, queries):
        lis = []
        fp = open(queries, "r")
        for line in fp:
            line = line.strip("\n")
            lis.append(line)
        return lis
    '''
    This method makes priority queue based on list of queries and webpage indexes
    '''
    def mkQueue(self, qLis, wLis):
        qs = []
        for q in qLis:
                qs.append(WebpagePriorityQueue(wLis,q))
        return qs 
    '''
    This method prints the priority queues of each query
    '''
    def processQ(self, pQ, qLis):
        i = 1
        for q in pQ:
            print("Query: %s" % qLis[(i-1)])
            if self.USL > len(q.queue):
                self.USL = len(q.queue)
            for num in range(0, self.USL):
                WPI = q.peek()
                print("Filename:%s" % os.path.basename(WPI.page.filename), end=", ")
                print("Priority: %d" % WPI.priority)
                q.poll()
            q.reheap(self.queries[i])
            i+=1
            print()                
    
def main():
    files = (r'C:\Users\NoorPC\Desktop\School\Cisc 235\test data\doc*.txt')
    query = (r'C:\Users\NoorPC\Desktop\School\Cisc 235\test data\queries.txt')
    processQueries(files, query,10)
    
main()

