from datetime import time

class truck:
    size = 16
    Clock = time(hour = 8)
    def __init__(self,id):
        self.id = id
        self.packages = [None] * self.size
        self.load = 0
        self.currentAddress = "HUB"

    def scan(self, ID):
        with open('scanLog.txt', 'a') as log:
            currentPackage = self.packageTable.packages[self.packageTable.searchById(ID)]
            log.write(str(currentPackage.id) + ' ' +  currentPackage.status + ' '  + "Scanned by driver\n")

    def truckFull(self):
        return self.load + 1 >= self.size
    
    def loadPackage(self, package):
        if not self.truckFull:
            package.status = self.Clock.strftime('%I:%M %p') + " Loaded on Truck " + self.id
            self.packages[self.load] = package
            self.load += 1
    def popById(self, id):
        i = 0
        for x in range(self.load):
            if self.packages[i].id == id:
                tempPackage = self.packages[i]
                self.packages[i] = None
                return tempPackage
        return None
    def packageSort(self, dispatch):
        i = 0
        tempList = [None] * self.size
        for x in range(self.load):
            nextId = dispatch.findNextPackage(self.currentAddress, self.packages)
            tempList[i] = self.packages.popById(nextId)
            i += 1
        self.packages = tempList
    def getRemainingSpace(self):
        return self.size - (self.load + 1) 