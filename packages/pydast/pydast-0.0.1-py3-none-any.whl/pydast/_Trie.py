class Trie:
    def __init__(self,val=None) -> None:
        self.is_end=False
        self.children={}
        if hasattr(val,'__iter__'):
            for item in val:
                self.add(item)

    def __contains__(self,word):
        return self.find(word)

    def add(self,s):
        for i in s:
            if i not in self.children:
                self.children[i]=Trie()
            self=self.children[i]
        self.is_end=True

    def find(self,s):
        for i in s:
            if i not in self.children:
                return False
            self=self.children[i]
        return self.is_end

    def remove(self,s):
        def rem(node,s,i):
            if i==len(s):
                node.is_end=False
                return not len(self.children)
            else:
                next=rem(node.children[s[i]],s,i+1)
                if next:
                    del self.children[s[i]]
                return next and not self.is_end and not len(self.children)
        
        if isinstance(s,str): rem(self,s,i)
        elif isinstance(s,list) or isinstance(s,tuple):
            for i in s: rem(self,i,0)

    def retrieve(self):
        def get(node,string,stings):
            if node.is_end:
                strings.append("".join(string))
            for ch in node.children:
                string.append(ch)
                get(node.children[ch],string,strings)
                string.pop()
        string=[]
        strings=[]
        get(self,string,strings)
        return strings

    def autocomplete(self,s):
        for i in s:
            if i not in self.children:
                return []
            self=self.children[i]
        return list(map(lambda x:s+x,self.retrieve()))