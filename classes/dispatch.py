#import classes.truck
from classes.package import package
from classes.hashTable import hashTbl
from collections import defaultdict
from datetime import time
from datetime import datetime
from classes.truck import truck
import csv
class dispatch:
    #assigment stratigy find furthest location from hub as farlocation and location fartest from farlocation as otherlocation then assgine trucks based off of 
    #distance from far location and other location 
    #routing idea  deliver closest locations 
    #loading idea load prios first then based off of distance no more then 16 packages per truck
    #start time is 8:00am
    #will recive 4 delayed packages 3 of witch need to be delivered by 1030 
    #package 2,36,38 must be on truck2 13,14,15,16,19,20 must be delivered togeather
    #find some way to assgine address ids maybe sum of numbers + leters ansii values 
    #track time per truck accumulated in a veriable held in truack to display status use loop in dispatch to check each truck 
    #address table with package ids and paclage count?? use address table to help loading function maybe a dictionary of dictionarys? 
    Clock = time(hour = 8)
    Trucks = [truck(1),truck(2)]
    EOD = datetime.strptime("5:00 PM", '%I:%M %p').time()  
    undeliveredPackages = []

    def loadAddresses(self):
        Distancelist = {}
        TestList = []
        i = 0
        with open('Distance.csv', newline='') as csvfile:
            Distancereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            TestList = next(Distancereader)
            for row in Distancereader:
                tempDic = {}
                tempint = 1
                for address in TestList:
                    tempDic[address] = {float(row[tempint])}
                    tempint += 1
                Distancelist[row[0]] = tempDic
        self.Distancelist = Distancelist

    
    def loadPackages(self):  
        packagelist = []
        addressDic = defaultdict(list)
        with open('WGUPSPackageFile.csv', newline='') as csvfile:
            packagereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in packagereader:
                packagelist.append(row)
            for row in packagelist:
                print(row)
        self.packageTable = hashTbl(len(packagelist))
        self.prioPackageList = hashTbl(len(packagelist))
        for row in packagelist:
            addressDic[row[1] + " " + row[4]].append(int(row[0]))
            tempPackage = package()
            tempPackage.id = int(row[0])
            tempPackage.address = row[1]
            tempPackage.City = row[2]
            tempPackage.State = row[3]
            tempPackage.Zip = row[4]
            if "EOD" not in row[5]:
                tempPackage.DeliveryDeadline = datetime.strptime(row[5], '%I:%M %p').time()
            else:
                tempPackage.DeliveryDeadline = self.EOD      
            if row[8] != '':
                tempPackage.truck = int(row[8])
            if row[9] != '':
                tempPackage.boundList = row[9].split()
            self.packageTable.add(tempPackage)
            if "Start"  in row[7]:
                tempPackage.status = self.Clock.strftime('%I:%M %p') + " Arrived at hub" 
                self.scan(tempPackage.id)
                self.undeliveredPackages.append(tempPackage)
        self.addressDic = addressDic
        self.BoundDel = False
        self.PrioDel = False
        self.TruckReq = False

    def findPackage(self,package):
        return self.packageTable.packages[self.packageTable.searchById(package.id)]
    def getDistance(self,startLocation,endLocation):
        
        return next(iter(self.Distancelist[startLocation][endLocation]))

    def resetScanLog(self):
        with open('scanLog.txt', 'w') as log:
            log.truncate()

    def scan(self, ID):
        with open('scanLog.txt', 'a') as log:
            currentPackage = self.packageTable.packages[self.packageTable.searchById(ID)]
            log.write(str(currentPackage.id) + ' ' +  currentPackage.status + ' '  + "Scanned at hub\n")

    def findNextPackage(self, currentAddress, Packages):
        distance = 100
        nextPackage = None
        for package in Packages:
            if package and (package != -1):
                if (self.getDistance(currentAddress, package.address + ' ' + package.Zip) < distance):
                    distance = self.getDistance(currentAddress, package.address + ' ' + package.Zip)
                    nextPackage = package
        if nextPackage == None:
            print("here")
        return nextPackage

    def loadTruck(self):
        if not self.PrioDel or not self.BoundDel or not self.TruckReq:
            self.loadSpecial()
            self.loadPrio()
        for truck in self.Trucks:
            while not truck.truckFull() and truck.returned and len(self.undeliveredPackages) > 0:
                tempPackage  = self.findNextPackage(truck.currentAddress,self.undeliveredPackages)
                if"hub" in tempPackage.status:
                    truck.loadPackage(tempPackage)
                self.undeliveredPackages.remove(tempPackage)
    def loadSpecial(self):
        truckFull = [False,False]
        for package in list(self.undeliveredPackages):
            if(package.truck > 0):
                if not self.Trucks[int(package.truck) - 1].truckFull():
                    self.Trucks[int(package.truck) - 1].loadPackage(self.findPackage(package))
                    self.undeliveredPackages.remove(package)
                else:
                    truckFull[0] = True
            elif(len(package.boundList) > 0 and "hub" in package.status):
                for truck in self.Trucks:
                    if(truck.getRemainingSpace() >= len(package.boundList)):
                        for item in package.boundList:
                            itemPackage = self.packageTable.packages[self.packageTable.searchById(item)]
                            truck.loadPackage(itemPackage)
                            self.undeliveredPackages.remove(itemPackage)
                            truckFull[1] = False
                        break
                    else:
                        truckFull[1] = True
            elif(package.DeliveryDeadline < self.EOD):
                self.prioPackageList.add(package)
        if not truckFull[0]:
            self.TruckReq = True
        if not truckFull[1]:
            self.BoundDel = True

    def loadPrio(self):
        trucksFull = False
        for truck in self.Trucks:
            truck.packageSort(self)
        for truck in self.Trucks:
            trucksFull = False
            while not truck.truckFull():
                tempPackage = self.findNextPackage(truck.currentAddress,self.prioPackageList.packages)
                if tempPackage and (tempPackage != -1) and "hub" in tempPackage.status:
                    self.prioPackageList.HashRemove(tempPackage.id)
                    truck.loadPackage(tempPackage)
                    truck.currentAddress = tempPackage.address + ' '
                    truck.currentAddress += tempPackage.Zip
                else:
                    break    
            trucksFull = True
        if not trucksFull:
            self.PrioDel = True

    def checkReturned(self):
        selectedTruck = self.Trucks[0]
        for truck in self.Trucks:
            if truck.Clock < selectedTruck.Clock:
                selectedTruck = truck
        selectedTruck.returned = True

    def wrongAddress(self, id):
        wrongAddresPackage =  self.packageTable.packages[self.packageTable.searchById(id)]
        self.undeliveredPackages.remove(wrongAddresPackage)

    def updateAddress(self, id, address, zip):
        wrongAddresPackage =  self.packageTable.packages[self.packageTable.searchById(id)]
        wrongAddresPackage.address = address
        wrongAddresPackage.zip = zip
        self.undeliveredPackages.append(wrongAddresPackage)