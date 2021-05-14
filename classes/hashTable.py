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
        if(self[curentPackage.hash] == False or self[curentPackage.hash] == -1):
            self[curentPackage.hash] = curentPackage
        else:
            i = 1
            size = self.size - 1
            while i <= self.size:
                if(i + curentPackage.hash> size):
                    if(not(self[i - curentPackage.hash]) or self[i - curentPackage.hash] == -1):
                        self[i - curentPackage.hash] = curentPackage
                else:
                    if(not(self[i + curentPackage.hash]) or self[i + curentPackage.hash] == -1):
                        self[i + curentPackage.hash] = curentPackage
    def passtest(curentPackage):
        curentPackage.id = 10
