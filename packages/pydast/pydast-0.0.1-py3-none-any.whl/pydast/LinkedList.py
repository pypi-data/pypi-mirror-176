
# & -----------------------------------------------------------------------------------------------------------
# & ---------------------------------------  Singly Linked List -----------------------------------------------
# & -----------------------------------------------------------------------------------------------------------

# Singly LinkedList
# Variables : head      tail        size        mutable     __itercurr
# Dunder Methods : __init__      __repr__
# Methods : append      extend      insert      pop     remove      indexof     makearr     reverse

class slnode:
    def __init__(self,Data=None,Next=None):
        self.val=Data
        self.next=Next

class singly:

    # > --------------------------------------- DUNDER METHODS ------------------------------------------------

    # *Constructor
    def __init__(self,val=None):
        self.head=None
        self.tail=None
        self.size=0

        # Iteration variables
        self.__itercurr=self.head

        # List initialization from val
        if hasattr(val,'__iter__'):
            for item in val:
                self.append(item)
        elif isinstance(val,slnode):
            self.head=val

    # *Representation
    def __repr__(self) -> str:
        return str(self)

    # *String Conversion
    def __str__(self) -> str:
        s=''
        if self.head==None:
            s=''
        else:
            l=[]
            curr=self.head
            while curr.next!=None:
                s+=str(curr.val)+" --> "
                curr=curr.next
            s+=str(curr.val)+" --> null"
        return s

    # *Iteration Method 
    def __iter__(self):
        self.__itercurr=self.head
        return self

    def __next__(self):
        if self.__itercurr==None:
            self.__itercurr=self.head
            raise StopIteration('Reached the End Node')
        else:
            temp=self.__itercurr.val
            self.__itercurr=self.__itercurr.next
            return temp

    # *Length Method
    def __len__(self):
        return self.size

    # *Operator Overloading
    def __iadd__(self,obj): # Operator : +=
        try:
            self.extend(obj)
            return self
        except:
            raise NotImplemented

    def __imul__(self,times): # Operator : *=
        return self

    def __ilshift__(self): # Operator : <<=
        return self

    def __irshift__(self): # Operator : >>=
        return self

    def __eq__(self,other): # Operator : ==
        return _compare(self,other)

    # > -------------------------------------------- CLASS METHODS --------------------------------------------

    # getHead
    def gethead(self):
        return self.head

    # Append Method
    def append(self,val):
        if self.head==None:
            self.head=self.tail=slnode(val)
        else:
            self.tail.next=slnode(val)
            self.tail=self.tail.next
        self.size+=1

    # Extend Method
    def extend(self,val):
        if isinstance(val,singly):
            for i in val.makearr():
                self.append(i)

        elif isinstance(val,list) or isinstance(val,tuple):
            for i in val:
                self.append(i)
        
    # Insert at Index Method
    def insert(self,pos,val):
        if pos<0:
            pos=self.size+pos
        if (pos>self.size-1 or pos<0) and not (self.size==0 and pos==0):
            raise IndexError("Index Not Found")
        if pos==0:
            self.head=slnode(val,self.head)
        else:
            curr=self.head
            for _ in range(pos-1):
                curr=curr.next
            curr.next=slnode(val,curr.next)
        self.size+=1

    # Pop Method # Needs Remodelling
    def pop(self,pos=-1):
        if pos<0:
            pos=self.size+pos
        if pos>=self.size or pos<0:
            raise IndexError("list index out of range")
        if pos==0:
            temp=self.head.val
            self.head=self.head.next
            self.size-=1
            return
        else:
            curr=self.head
            for _ in range(pos-1):
                curr=curr.next
            temp=curr.next.val
            curr.next=curr.next.next
            if curr.next==self.tail:
                self.tail=curr
        if pos==self.size-1:
            curr=self.head
            while curr.next!=None:
                curr=curr.next
            self.tail=curr
        self.size-=1
        return temp

    # Remove element # Not-Fixed
    def remove(self,val):
        if self.head.val==val:
            self.head=self.head.next
            self.size-=1
            return
        curr=self.head
        while curr.next!=None:
            if curr.next.val==val:
                if curr.next==self.tail:
                    self.tail=curr
                curr.next=curr.next.next
                self.size-=1
                return
            curr=curr.next
        raise ValueError("Value Not Found")

    # Find Index
    def indexof(self,val):
        curr=self.head
        for i in range(self.size):
            if curr.val==val:
                return i
            curr=curr.next
        return -1

    # Sorting
    def sort(self):
        ptr1=self.head
        ptr2=self.head
        while ptr1 is not None:
            ptr2=ptr1
            while ptr2.next is not None:
                if ptr2.val>ptr2.next.val:
                    ptr2.next.next,ptr2.next,=ptr2=ptr2.next.next
                else:
                    ptr2=ptr2.next
            ptr1=ptr1.next

    # To str
    # def tostr(self):
    #     s=''
    #     if self.head==None:
    #         s=''
    #     else:
    #         l=[]
    #         curr=self.head
    #         while curr.next!=None:
    #             s+=str(curr.val)+" --> "
    #             curr=curr.next
    #         s+=str(curr.val)
    #     return s
    
    # Print Linked List Method 
    # def print(self):
    #     print(self)
    
    # Make Array Method
    # def makearr(self):
    #     if self.head==None:
    #         return []
    #     else:
    #         l=[]
    #         curr=self.head
    #         while curr.next!=None:
    #             l.append(curr.val)
    #             curr=curr.next
    #         l.append(curr.val)
    #         return l

    # Reversing
    def reverse(self):
        if self.size<=1:
            return
        self.tail=self.head
        curr=self.head
        next=self.head.next
        prev=None
        while next != None:
            curr.next=prev
            prev=curr
            curr=next
            next=curr.next
        curr.next=prev
        self.head=curr

    # Sorting
    def sort(self,reverse=False):
        if not reverse:

            # Initialization Pointer
            curr=self.head
            curr2=self.head
            
            # Setting head to the minimum value
            curr3=self.head
            while curr!=None:
                if curr.val<self.head.val:
                    self.head=curr
                curr=curr.next
            
            # Begining sorting
            while curr is not None:
                curr2=curr
                while curr2 is not None and curr2.next is not None:

                    curr2=curr2.next
                curr=curr.next

    # > ---------------------------------- PRIVATE STATIC METHODS ---------------------------------------------

# ? --------------------------------------- INHERITED CLASS STACK ---------------------------------------------

class Stack (singly):

    # Constuctor
    def init(self):
        self.top=None

# > ------------------------------------------- stack methods --------------------------------------------------
    
    def push(self,val):
        self.insert(0,val)
        self.top=self.head
    
    def pop(self):
        resval = self.pop()
        self.top=self.head
        return resval

    def peek(self):
        return self.top.val

# ? -------------------------------------- INHERITED CLASS QUEUE -----------------------------------------------

class Queue (singly):

    # Constructor
    def init(self):
        self.front=None
        self.end=None

    # > -------------------------------------- queue methods ---------------------------------------------------

    def enqueue(self,val):
        self.append(val)

    def dequeue(self):
        return self.pop(0)

    def isempty(self):
        return not bool(self.size)

# & -----------------------------------------------------------------------------------------------------------
# & ---------------------------------------  Doubly Linked List -----------------------------------------------
# & -----------------------------------------------------------------------------------------------------------

# Doubly LinkedList
# Methods : append      extend      insert      pop     remove      indexof     print       makearr
#           reverse

class dlnode:
    def __init__(self,Data=None,Prev=None,Next=None):
        self.val=Data
        self.prev=Prev
        self.next=Next

class doubly:

    # > ------------------------------------------ MAGIC METHODS --------------------------------------------
    # * Constructor
    def __init__(self,val=None):
        self.head=None
        self.tail=None
        self.size=0

        # *Iteration variables
        self.__itercurr=self.head

        # *Initialization with val
        if isinstance(val,list) or isinstance(val,tuple):
            self.extend(val)


    # * Representation Method
    def __repr__(self) -> str:
        return self.tostr()
        
    # *Iteration Method 
    def __iter__(self):
        self.__itercurr=self.head
        return self

    def __next__(self):
        if self.__itercurr==None:
            self.__itercurr=self.head
            raise StopIteration('Reached the End Node')
        else:
            temp=self.__itercurr.val
            self.__itercurr=self.__itercurr.next
            return temp

    # > ----------------------------------------- CLASS METHODS --------------------------------------------
    # Append Method
    def append(self,val):
        if self.head==None:
            self.head=self.tail=dlnode(val)
        else:
            self.tail.next=dlnode(val,self.tail)
            self.tail=self.tail.next
        self.size+=1

    # Extend Method
    def extend(self,val):
        n=len(val)
        if n==0:
            return
        for i in val:
            self.append(i)

    # Insert Method
    def insert(self,pos,val):
        if pos<0:
            pos=self.size+pos
        if pos<0 or pos>=self.size:
            raise IndexError("Index Not Found")
        if pos==0:
            self.head=dlnode(val,None,self.head)
            self.head.next.prev=self.head
            self.size+=1
        else:
            curr=self.head
            for _ in range(pos-1):
                curr=curr.next
            curr.next=dlnode(val,curr,curr.next)
            curr.next.next.prev=curr.next
            self.size+=1

    # Pop Method 
    def pop(self,pos=-1):
        if pos<0:
            pos=self.size+pos
        if pos<0 or pos>=self.size:
            raise IndexError("Index Not Found")
        if pos==0:
            self.head=self.head.next
            self.head.prev=None
        elif pos==self.size-1:
            self.tail=self.tail.prev
            self.tail.next=None
        else:
            curr=self.head
            for _ in range(pos-1):
                curr=curr.next
            curr.next=curr.next.next
            curr.next.prev=curr
        self.size-=1

    # Remove Method
    def remove(self,val):
        if self.head.val==val:
            self.head=self.head.next
            self.head.prev=None
        elif self.tail.val==val:
            self.tail=self.tail.prev
            self.tail.next=None
        else:
            curr=self.head
            flag=1
            while curr.next!=None:
                if curr.next.val==val:
                    curr.next=curr.next.next
                    curr.next.prev=curr
                    flag=0
                    self.size-=1
                    return
                curr=curr.next
            raise ValueError("Value Not Found")
        self.size-=1

    # Index of Method
    def indexof(self,val):
        curr=self.head
        for i in range(self.size-1):
            if curr.val==val:
                return i
            curr=curr.next
        return -1

    # Tostr function
    def tostr(self,reverse=False):
        s=''
        if reverse:
            if self.size:
                s=''
                curr=self.tail
                while curr.prev!=None:
                    s+=str(curr.val)+"<--> "
                    curr=curr.prev
                s+=str(curr.val)
        else:
            if self.size:
                curr=self.head
                while curr.next!=None:
                    s+=str(curr.val)+" <--> "
                    curr=curr.next
                s+=str(curr.val)
        return s

    # Make Array Method
    def makearr(self,reverse=False):
        if self.size==0:
            return []
        l=[]
        if reverse:
            curr=self.tail.prev
            while curr.prev!=None:
                l.append(curr.val)
                curr=curr.prev
            l.append(curr.val)
        else:
            l=[]
            curr=self.head
            while curr.next!=None:
                l.append(curr.val)
                curr=curr.next
            l.append(curr.val)
        return l

    # Print Method 
    def print(self,reverse=False):
        if reverse:
            if self.size==0:
                print("Empty List")
            else:
                curr=self.tail
                while curr.prev!=None:
                    print(curr.val,"<--> ",end="")
                    curr=curr.prev
                print(curr.val)
                return self.size
        else:
            if self.size==0:
                print("Empty List")
            else:
                curr=self.head
                while curr.next!=None:
                    print(curr.val,"<--> ",end="")
                    curr=curr.next
                print(curr.val)
                return self.size

    # Make Array Method
    def makearr(self,reverse=False):
        if self.size==0:
            return []
        l=[]
        if reverse:
            curr=self.tail.prev
            while curr.prev!=None:
                l.append(curr.val)
                curr=curr.prev
            l.append(curr.val)
        else:
            l=[]
            curr=self.head
            while curr.next!=None:
                l.append(curr.val)
                curr=curr.next
            l.append(curr.val)
        return l

    # Reversing
    def reverse(self):
        curr=self.head
        while curr!=None:
            curr.next,curr.prev=curr.prev,curr.next
            curr=curr.prev
        self.head,self.tail=self.tail,self.head


    
    # *--------------------------------------- SUBCLASS STACK -----------------------------------------------

    
    # *--------------------------------------- SUBCLASS QUEUE -----------------------------------------------


# & ---------------------------------------------------------------------------------------------------------
# & ---------------------------------------- Module Functions -----------------------------------------------
# & ---------------------------------------------------------------------------------------------------------
# Module Functions

# Compare two Linked List
def _compare(list1,list2) -> bool:
    if (isinstance(list1,singly) and isinstance(list2,singly)) or (isinstance(list1,doubly) and isinstance(list2,doubly)):
        curr1,curr2=list1.head,list2.head
        while curr1!=None and curr2!=None:
            if curr1.val!=curr2.val:
                return False
            curr1,curr2=curr1.next,curr2.next
        if curr2!=None or curr1!=None:
            return False
        return True
    else:
        raise TypeError("Both arguments should be same type being either singly or doubly")

# Merge Two Sorted Linked Lists
def mergeSortedLists(list1,list2):
    if (isinstance(list1,singly) and isinstance(list2,singly)):
        new=slnode(None)
        newcurr=new
        while True:
            if head1==head2==None:
                break
            if head1==None:
                newcurr.next=head2
                break
            if head2==None:
                newcurr.next=head1
                break
            if head1.val<head2.val:
                newcurr.next=head1
                head1=head1.next
            else:
                newcurr.next=head2
                head2=head2.next
            newcurr=newcurr.next
        return new.next