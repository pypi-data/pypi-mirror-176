
# & ------------------------------------------------------------------------------------------------------------
# & ------------------------------------------------- MinHeap --------------------------------------------------
# & ------------------------------------------------------------------------------------------------------------

# User Methods : isempty    push    pop     peek

class minHeap:
    
    # >------------------------------------------- dunder methods ---------------------------------------------------
    
    def __init__(self,arr=[],key=lambda x:x) -> None:
        self.__key=key
        self.__heap=list(arr)
        self.__heapify()
    
    def __iadd__(self,val):               # O(log n)
        self.push(val)   
        return self

    def __len__(self):                    # O(1)
        return len(self.__heap)

    # >------------------------------------------- private methods ---------------------------------------------------

    def __heapifyup(self,index):          # O(log n)  # working great
        while index:
            parent=(index-1)//2
            if self.__key(self.__heap[parent])>self.__key(self.__heap[index]):
                self.__heap[parent],self.__heap[index]=self.__heap[index],self.__heap[parent]
            index=parent

    def __heapifydown(self,index):        # O(log n)  # working great
        left= (2*index) +1
        right=(2*index) +2
        while (left<len(self.__heap) and self.__key(self.__heap[left])<self.__key(self.__heap[index])) or (right<len(self.__heap) and self.__key(self.__heap[right])<self.__key(self.__heap[index])):
            smaller=left if (right>=len(self.__heap)) or (self.__key(self.__heap[left])<self.__key(self.__heap[right])) else right
            self.__heap[index],self.__heap[smaller]=self.__heap[smaller],self.__heap[index]
            index=smaller
            left=(2*index)+1
            right=(2*index)+2
    
    def __heapify(self):                    # O(n)
        for i in range(len(self.__heap)-1,-1,-1):
            self.__heapifydown(i)

    # >------------------------------------------- public methods ---------------------------------------------------
    
    def getmin(self):
        return min(self.__heap)

    def isempty(self):                    # O(1) 
        return not bool(len(self.__heap))

    def push(self,val):                   # O(log n)
        self.__heap.append(val)
        self.__heapifyup(len(self.__heap)-1)
    
    def pop(self):                        # O(log n)
        if self.isempty(): return None
        self.__heap[0],self.__heap[len(self.__heap)-1]=self.__heap[len(self.__heap)-1],self.__heap[0]
        res=self.__heap.pop()
        self.__heapifydown(0)
        return res

    def peek(self):
        if self.isempty(): return None                      # O(1)
        return self.__heap[0]

# & ------------------------------------------------------------------------------------------------------------
# & ------------------------------------------------- MaxHeap --------------------------------------------------
# & ------------------------------------------------------------------------------------------------------------

# Key setup to be added
class maxHeap:
    
    # >------------------------------------------- dunder methods ---------------------------------------------------
    
    def __init__(self,arr=[],key=lambda x:x) -> None:   # O(n)
        self.__key=key
        self.__heap=arr
        self.__heapify()

    def __iadd__(self,val):             # O(log n)
        self.push(val)
        return self

    def __len__(self):
        return len(self.__heap)

    # >------------------------------------------- private methods ---------------------------------------------------

    def __heapifyup(self,index):        # O(log n)
        while index:
            parent=(index-1)//2
            if self.__key(self.__heap[parent])<self.__key(self.__heap[index]):
                self.__heap[parent],self.__heap[index]=self.__heap[index],self.__heap[parent]
            index=parent

    def __heapifydown(self,index):      # O(log n)
        left= (2*index) +1
        right=(2*index) +2
        while (left<len(self.__heap) and self.__key(self.__heap[left])>self.__key(self.__heap[index])) or (right<len(self.__heap) and self.__key(self.__heap[right])>self.__key(self.__heap[index])):
            smaller=left if (right>=len(self.__heap)) or (self.__key(self.__heap[left])>self.__key(self.__heap[right])) else right
            self.__heap[index],self.__heap[smaller]=self.__heap[smaller],self.__heap[index]
            index=smaller
            left=(2*index)+1
            right=(2*index)+2

    def __heapify(self):                # O(n)
        for i in range(len(self.__heap)-1,-1,-1):
            self.__heapifydown(i)
    
    # >------------------------------------------- public methods ---------------------------------------------------

    def isempty(self):                  # O(1)
        return not bool(len(self))

    def push(self,val):                 # O(log n)
        self.__heap.append(val)
        self.__heapifyup(len(self.__heap)-1)

    def pop(self):                      # O(log n)
        if self.isempty(): return None
        self.__heap[0],self.__heap[len(self.__heap)-1]=self.__heap[len(self.__heap)-1],self.__heap[0]
        res=self.__heap.pop()
        self.__heapifydown(0)
        return res

    def peek(self):                     # O(1)
        if self.isempty(): return None
        return self.__heap[0]