from datetime import datetime, time, timedelta

from classes import package


class truck:
    size = 16
    Clock = time(hour=8)

    def __init__(self, id):
        self.id = id
        self.packages = [None] * self.size
        self.load = 0
        self.currentAddress = "HUB"
        self.returned = True
        self.miles = 0
        self.boundPackageOnboard = False
        self.emergencyReturn = False
        self.returnNow = False

    # scans the package and adds it to the log
    def scan(self, currentPackage):
        if currentPackage.status == "Delivered":
            currentPackage.time = self.Clock
        with open('scanLog.txt', 'a') as log:
            log.write(str(currentPackage.id) + ' ' + currentPackage.status + ' ' + "Scanned by driver\n")

    # lets us know when truck is full
    def truckFull(self):
        return self.load >= self.size

    # adds package to truck list
    def loadPackage(self, package):
        if package:
            if len(package.boundList) > 0:
                self.boundPackageOnboard = True;
            if not self.truckFull():
                package.status = self.Clock.strftime('%I:%M %p') + " Loaded on Truck " + str(self.id)
                self.scan(package)
                self.packages[self.load] = package
                self.load += 1

    # removes package based off of id
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

    # sorts the package based of nearest neighbor
    def packageSort(self, dispatch):
        i = 0
        tempList = [None] * self.size
        for x in range(self.load):
            nextId = dispatch.findNextPackage(self.currentAddress, self.packages, "Loaded")
            if nextId is not None:
                self.currentAddress = nextId.address + ' ' + nextId.Zip
                tempList[i] = self.popById(nextId.id)
                i += 1
        self.packages = tempList

    # returns how much space is remaining on the truck
    def getRemainingSpace(self):
        return self.size - (self.load + 1)

    # converts the distance traveled to time traveled
    def getDistanceAsTime(self, distance):
        distance = distance * 3.33
        minute = int(distance)
        second = distance - minute
        second = int(second * 1000 * .06)
        return timedelta(minutes=minute, seconds=second)

    # sets the clock to new time
    def setClock(self, newTime):
        hours = int(newTime / 3600)
        minutes = int((newTime % 3600) / 60)
        seconds = (newTime % 3600) % 60
        self.Clock = time(hour=hours, minute=minutes, second=seconds)

    # updates time based off of distance travled
    def updateTime(self, distance):
        self.miles = self.miles + distance
        tempTime = timedelta(hours=self.Clock.hour, minutes=self.Clock.minute, seconds=self.Clock.second) + (
            self.getDistanceAsTime(distance))
        self.setClock(tempTime.seconds)
        if tempTime > timedelta(hours=9, minutes=30):
            if not self.boundPackageOnboard:
                if not self.emergencyReturn:
                    self.emergencyReturn = True
                    self.returnNow = True

    # deliivers packages on truck
    def deliverLoad(self, dispatch):
        self.currentAddress = "HUB"
        for package in self.packages:
            if (package != None and "Loaded" in package.status):
                if self.returnNow:
                    package.status = "Undelivered"
                else:
                    distance = dispatch.getDistance(self.currentAddress, package.getShippingAddress())
                    self.updateTime(distance)
                    self.currentAddress = package.getShippingAddress()
                    package.status = self.Clock.strftime('%I:%M %p') + " Delivered by truck " + str(
                        self.id)
                    self.scan(package)
                    self.popById(package.id)
        distance = dispatch.getDistance(self.currentAddress, "HUB")
        self.updateTime(distance)
        self.currentAddress = "HUB"
        self.load = 0
        self.returned = False
        self.returnNow = False

    # unloads package
    def Unload(self, dispatch):
        for package in self.packages:
            if (package != None and "Loaded" in package.status):
                package.status = "Undelivered"
                dispatch.scan(package.id)

    # adds package to frint of list
    def appendPackage(self, selectedPackage: package):
        tempPackage = self.packages[0]
        self.packages[0] = selectedPackage
        self.packages[self.load] = tempPackage
        self.load += 1
        self.currentAddress = selectedPackage.address + ' ' + selectedPackage.Zip
