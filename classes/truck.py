from datetime import datetime, time, timedelta

class truck:
    size = 16
    Clock = time(hour = 8)
    def __init__(self,id):
        self.id = id
        self.packages = [None] * self.size
        self.load = 0
        self.currentAddress = "HUB"

    def scan(self, currentPackage):
        with open('scanLog.txt', 'a') as log:
            log.write(str(currentPackage.id) + ' ' +  currentPackage.status + ' '  + "Scanned by driver\n")

    def truckFull(self):
        return self.load >= self.size
    
    def loadPackage(self, package):
        if not self.truckFull():
            package.status = self.Clock.strftime('%I:%M %p') + " Loaded on Truck " + str(self.id)
            self.scan(package)
            self.packages[self.load] = package
            self.load += 1
    def popById(self, id):
        i = 0
        for x in range(self.load):
            if self.packages[i] != None and self.packages[i].id == id:
                tempPackage = self.packages[i]
                self.currentAddress = tempPackage.address + ' '
                self.currentAddress += tempPackage.Zip
                self.packages[i] = None
                return tempPackage
            i += 1
        return None
    def packageSort(self, dispatch):
        i = 0
        tempList = [None] * self.size
        for x in range(self.load):
            nextId = dispatch.findNextPackage(self.currentAddress, self.packages)
            tempList[i] = self.popById(nextId.id)
            i += 1
        self.packages = tempList
    def getRemainingSpace(self):
        return self.size - (self.load + 1) 
    def getDistanceAsTime(self, distance):
        minute = int(distance) 
        second = distance - minute
        second = int(second*1000*.06)
        return timedelta(minutes=minute,seconds=second)
    def setClock(self,newTime):
        hours = int(newTime/3600)
        minutes = int((newTime%3600)/60)
        seconds = (newTime%3600)%60
        self.Clock = time(hour=hours ,minute=minutes,second=seconds)
    def updateTime(self,distance):
        distance = self.getDistanceAsTime(distance)
        tempTime = timedelta(hours=self.Clock.hour, minutes=self.Clock.minute,seconds = self.Clock.second) + distance
        self.setClock(tempTime.seconds)
    def deliverLoad(self,dispatch):
        self.currentAddress = "HUB"
        for package in self.packages:
            if(package != None and "Loaded" in package.status):
                distance = dispatch.getDistance(self.currentAddress,package.getShippingAddress())
                self.updateTime(distance)
                self.currentAddress = package.getShippingAddress()
                package.status = self.Clock.strftime('%I:%M %p') + " Delivered by truck " + str(self.id)
                self.scan(package)
                self.popById(package.id)
        distance = dispatch.getDistance(self.currentAddress,"HUB")
        self.updateTime(distance)
        self.currentAddress = "HUB"
        self.load = 0
