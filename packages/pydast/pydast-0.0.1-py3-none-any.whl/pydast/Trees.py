
# & ------------------------------------------------------------------------------------------------------------
# & ---------------------------------------------- Imports -----------------------------------------------------
# & ------------------------------------------------------------------------------------------------------------
from LinkedList import Stack
from LinkedList import Queue
# & ------------------------------------------------------------------------------------------------------------
# & -------------------------------------------- Binary Tree ---------------------------------------------------
# & ------------------------------------------------------------------------------------------------------------

class btnode:
    def __init__(self,Data=None,Left=None,Right=None):
        self.data=Data
        self.left=Left
        self.right=Right
        
class binarytree:
    def __init__(self,Node=None):
        self.root=None
        
        # *Traversal variable
        self.__traverse="pre"

        # *Iteration variable
        self.__traversalstack=[self.root]

    # >----------------------------------------- DUNDER METHODS ---------------------------------------------

    def __iter__(self):
        self.__traversalstack=[self.root]
        return self

    def __next__(self):
        if not len(self.__traversalstack):
            self.__traversalstack=[self.root]
            raise StopIteration

        if self.__traverse=="pre":
            curr=self.__traversalstack.pop()
            if curr.right!=None:
                self.__traversalstack.append(curr.right)
            if curr.left!=None:
                self.__traversalstack.append(curr.left)
            return curr.data

    # >------------------------------------------ USER METHODS ----------------------------------------------

    # Set Traversal Method
    def set_traversal(self,val):
        if val in ("pre","in","post","level"):
            self.__traverse=val
        else:
            raise ValueError("Traversal Mode Not Recognized")

    def left_sib_right_child(self):
        def lsrc(root,put=None):
            if root is None: return
            temp=root.left
            root.left=put
            lsrc(root.left)
            lsrc(root.right,temp)
        lsrc(self.root)
    
    def print_pretty(self):
        def prettyPrintTree(node, prefix="", isLeft=True):
            if not node:
                print("Empty Tree")
                return

            if node.right:
                prettyPrintTree(node.right, prefix + ("│   " if isLeft else "    "), False)

            print(prefix + ("└── " if isLeft else "┌── ") + str(node.data))

            if node.left:
                prettyPrintTree(node.left, prefix + ("    " if isLeft else "│   "), True)
        prettyPrintTree(self.root)

    # Insertion
    def insert(self,val):
        if self.root==None:
            self.root=btnode(val)
        else:
            curr=self.root
            while True:
                if val<curr.data:
                    if curr.left==None:
                        curr.left=btnode(val)
                        break
                    curr=curr.left
                else:
                    if curr.right==None:
                        curr.right=btnode(val)
                        break
                    curr=curr.right

    # Height Method
    def height(self):
        return binarytree.__height(self.root)

    # Lowest Common Ancestor
    def lca(self,v1,v2):
        return binarytree.__lca(self.root,v1,v2).data

    # LevelOrder Traversal
    def levelorder(self):
        if self.root==None:
            return []
        resarray=[]
        q=[]
        q.insert(0,self.root)
        while len(q):
            curr=q.pop()
            resarray.append(curr.data)
            if curr.left!=None:
                q.insert(0,curr.left)
            if curr.right!=None:
                q.insert(0,curr.right)
        return resarray

    # PreOrder Traversal
    def preorder(self):
        if self.root==None:
            return []
        resarray=[]
        s=[self.root]
        while len(s):
            curr=s.pop()
            resarray.append(curr.data)
            if curr.right!=None:
                s.append(curr.right)
            if curr.left!=None:
                s.append(curr.left)
        return resarray

    def inorder (self):
        if self.root==None:
            return []
        resarray=[]
        s=[self.root]

    def postorder(self):
        if self.root==None:
            return[]

    # Topview of the Tree
    def topView(self):
        res=[self.root.data]
        lmax=rmax=0
        q=[[self.root,0]]
        while len(q):
            curr,pos=q.pop()
            if curr==None:
                continue
            if pos<lmax:
                res.insert(0,curr.data)
                lmax=pos
            if pos>rmax:
                res.append(curr.data)
                rmax=pos
            q.insert(0,[curr.left,pos-1])
            q.insert(0,[curr.right,pos+1])
        return res

    # >----------------------------------------- UNACCESSIBLE METHODS ---------------------------------------

    # Height of the tree
    @staticmethod
    def __height(root):
        if root==None:
            return -1
        else:
            return max(binarytree.__height(root.left),binarytree.__height(root.right))+1

    # Lowest Common ancestor
    @staticmethod
    def __lca(root, v1, v2):
        if root==None:
            return 0
        if root.data in (v1,v2):
            return root
        else:
            a=binarytree.__lca(root.left,v1,v2)
            b=binarytree.__lca(root.right,v1,v2)
            if a and b:
                return root
            if not a:
                return b
            if not b:
                return a

# ? -------------------------------------------- Inherited Class Heap --------------------------------------

class heap(binarytree):

    def __init__(self, Node=None):
        pass

# & ------------------------------------------------------------------------------------------------------------
# & ----------------------------------------- Fenwick Tree -----------------------------------------------------
# & ------------------------------------------------------------------------------------------------------------

class BinaryIndexedTree:
    def __init__(self,nums):
        self.nums=nums
        self.tree=[0 for _ in range(len(nums)+1)]
        for i in range(len(nums)):
            index=i+1
            while index<len(self.tree):
                self.tree[index]+=nums[i]
                index+=index&-index

    def __len__(self):
        return len(self.nums)

    def getNums(self):
        return self.nums

    def __prefixSum(self,index):
        tot=0
        while index:
            print(index)
            tot+=self.tree[index]
            index-=(index&-index)
        return tot

    def update(self,index,val):
        diff=val-self.nums[index]
        self.nums[index]=val
        index+=1
        while index<len(self.tree):
            self.tree[index]+=diff
            index+= (index&-index)

    def getSum(self,l,r=None):
        if r==None: 
            return self.__prefixSum(l+1)
        else: 
            return self.__prefixSum(r+1)-self.__prefixSum(l)