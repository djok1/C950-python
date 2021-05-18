import classes.package
class hashTbl:
    def __init__(self,size):
        self.size = size
        self.map = [False] * self.size
    
    def _get_hash(self, key):
        hash = key % self.size
        return hash
    # ended up deciding to use -1 to indicate there has been a value as 1 == true returns true
    def add(self, curentPackage):
        curentPackage.hash = self._get_hash(curentPackage.id)
        if(self.map[curentPackage.hash] == False or self.map[curentPackage.hash] == -1):
            self.map[curentPackage.hash] = curentPackage
        else:
            i = 1
            size = self.size - 1
            while i <= self.size:
                if(i + curentPackage.hash> size):
                    if(not(self.map[i - curentPackage.hash]) or self.map[i - curentPackage.hash] == -1):
                        self.map[i - curentPackage.hash] = curentPackage
                        break
                else:
                    if(not(self.map[i + curentPackage.hash]) or self.map[i + curentPackage.hash] == -1):
                        self.map[i + curentPackage.hash] = curentPackage
                        break
                i += 1
            if(i > self.size):
                print("error:Table overflow")
                        
    def passtest(curentPackage):
        curentPackage.id = 10

    def _print(self):
        i = 0
        print('current package ids')
        while i < self.size:
            if(not(self.map[i]) or self.map[i] == -1):
                print(self.map[i])
            else:
                print(self.map[i].id)
            i += 1
    
    def HashRemove(self, id):
        location = self.searchById(id)
        remove = self.map[location]
        remove._print()
        print( " removed")
        self.map[location] = -1
        
        return remove
    
    def searchById(self, id):
        idHash = self._get_hash(id)
        i = 0
        size = self.size - 1
        while i <= self.size:
            if(i + idHash > size):
                if(self.map[i - idHash].id==idHash):
                    return i - idHash
                    break
                elif(not(self.map[i - idHash])):
                    break
            else:
                if(self.map[i + idHash].id==idHash):
                    return i + idHash
                    break
                elif(not(self.map[i - idHash])):
                    break
            
            i += 1
        print("id not found")
        return -1