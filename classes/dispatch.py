# import classes.truck
from classes.package import package
from classes.hashTable import hashTbl
from collections import defaultdict
from datetime import time, timedelta
from datetime import datetime
from classes.truck import truck
import csv


class dispatch:
    # assigment stratigy find furthest location from hub as farlocation and location fartest from farlocation as otherlocation then assgine trucks based off of
    # distance from far location and other location
    # routing idea  deliver closest locations
    # loading idea load prios first then based off of distance no more then 16 packages per truck
    # start time is 8:00am
    # will recive 4 delayed packages 3 of witch need to be delivered by 1030
    # package 2,36,38 must be on truck2 13,14,15,16,19,20 must be delivered togeather
    # find some way to assgine address ids maybe sum of numbers + leters ansii values
    # track time per truck accumulated in a veriable held in truack to display status use loop in dispatch to check each truck
    # address table with package ids and paclage count?? use address table to help loading function maybe a dictionary of dictionarys?
    Clock = time(hour=8)
    Trucks = [truck(1), truck(2)]
    EOD = datetime.strptime("5:00 PM", '%I:%M %p').time()

    # loads addresses into the distance list dictionary
    def loadAddresses(self):
        Distancelist = {}
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

    # loads the packages into the package table
    def loadPackages(self):
        packagelist = []
        addressDic = defaultdict(list)
        with open('WGUPSPackageFile.csv', newline='') as csvfile:
            packagereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in packagereader:
                packagelist.append(row)
        self.packageTable = hashTbl(len(packagelist))
        for row in packagelist:
            addressDic[row[1] + " " + row[4]].append(int(row[0]))
            tempPackage = package()
            tempPackage.id = int(row[0])
            tempPackage.address = row[1]
            tempPackage.City = row[2]
            tempPackage.State = row[3]
            tempPackage.Zip = row[4]
            tempPackage.weight = row[6]
            if "EOD" not in row[5]:
                tempPackage.DeliveryDeadline = datetime.strptime(row[5], '%I:%M %p').time()
            else:
                tempPackage.DeliveryDeadline = self.EOD
            if row[8] != '':
                tempPackage.truck = int(row[8])
            if row[9] != '':
                tempPackage.boundList = row[9].split()
            self.packageTable.add(tempPackage)
            if "Start" in row[7]:
                tempPackage.status = self.Clock.strftime('%I:%M %p') + " Arrived at hub"
                self.scan(tempPackage.id)
                tempPackage.status = "Undelivered"
            else:
                tempPackage.status = self.Clock.strftime('%I:%M %p') + " On way to Hub"
                self.lateScan(tempPackage.id)
        self.addressDic = addressDic
        self.wrongAddress(9)

    # returns the distance between addresses
    def getDistance(self, startLocation, endLocation):
        return next(iter(self.Distancelist[startLocation][endLocation]))

    # resets the scan log
    def resetScanLog(self):
        with open('scanLog.txt', 'w') as log:
            log.truncate()

    # writes the package to the scan log
    def scan(self, ID):
        with open('scanLog.txt', 'a') as log:
            currentPackage = self.packageTable.packages[self.packageTable.searchById(ID)]
            log.write(str(currentPackage.id) + ' ' + currentPackage.status + ' ' + "Scanned at hub\n")

    # O^N finds the next closest package
    def findNextPackage(self, currentAddress, packages, key: str):
        distance = 100
        nextPackage = None
        for selectedPackage in packages:
            if selectedPackage is not None:
                if key in selectedPackage.status:
                    if self.getDistance(currentAddress, selectedPackage.address + ' ' + selectedPackage.Zip) < distance:
                        distance = self.getDistance(currentAddress, selectedPackage.address + ' ' + selectedPackage.Zip)
                        nextPackage = selectedPackage
        if nextPackage is None:
            self.packageTable.allDelivered = True
        return nextPackage

    # write big O sepretly then bring them together
    # O(LogN) Loads any empty trucks after checking for time sensitive items
    def loadTruck(self):
        if self.Clock > time(hour=9, minute=5):
            self.reciveLates()
        if self.Clock > time(hour=10, minute=20):
            self.updateAddress(9, '410 S State St', '84111')
        for truck in self.Trucks:
            self.EmergencyLoad(truck)
            while not truck.truckFull() and truck.returned > 0:
                tempPackage = self.findNextPackage(truck.currentAddress, self.packageTable.packages, "Undelivered")
                if tempPackage is not None:
                    if tempPackage.truck == truck.id or tempPackage.truck < 0:
                        truck.loadPackage(tempPackage)
                        truck.currentAddress = tempPackage.address + ' ' + tempPackage.Zip
                    else:
                        tempPackage.status = "Skip"
                if tempPackage is None:
                    break

    # O(N) checks if any trucks are done with deliveries
    def checkReturned(self):
        selectedTruck = self.Trucks[0]
        for truck in self.Trucks:
            if truck.Clock < selectedTruck.Clock:
                selectedTruck = truck
        selectedTruck.returned = True
        self.Clock = selectedTruck.Clock

    # sets the package status wrong address
    def wrongAddress(self, id):
        wrongAddresPackage = self.packageTable.packages[self.packageTable.searchById(id)]
        wrongAddresPackage.status = "Wrong Address"

    # updates the address of the package with a wrong address
    def updateAddress(self, id, address, zip):
        wrongAddresPackage = self.packageTable.packages[self.packageTable.searchById(id)]
        if wrongAddresPackage.status == "Wrong Address":
            wrongAddresPackage.address = address
            wrongAddresPackage.Zip = zip
            wrongAddresPackage.status = "Undelivered"

    # O(N) updates the status on late packages so they can be loaded
    def reciveLates(self):
        for package in self.packageTable.packages:
            if "On way to Hub" in package.status:
                package.status = self.Clock.strftime('%I:%M %p') + " Arrived at hub"
                self.scan(package.id)
                package.status = "Undelivered"

    # O(N) loads any package that has a delivery deadline
    def EmergencyLoad(self, selectedTruck: truck):
        packageLoaded = False
        for selectedPackage in self.packageTable.packages:
            if "Skip" in selectedPackage.status:
                selectedPackage.status = "Undelivered"
            if selectedPackage.DeliveryDeadline != self.EOD:
                if "Undelivered" in selectedPackage.status:
                    if not selectedTruck.truckFull():
                        packageLoaded = True
                        selectedTruck.loadPackage(selectedPackage)
                    else:
                        selectedTruck.packageSort(self)
                        selectedTruck.deliverLoad(self)
        if packageLoaded:
            selectedTruck.packageSort(self)

    # O(N) loads packages that have to be delivered together into same truck
    def loadBound(self, selectedTruck: truck):
        earlyPackage = self.packageTable.packages[self.packageTable.searchById(15)]
        if len(earlyPackage.boundList) > 0 & len(earlyPackage.boundList) < selectedTruck.getRemainingSpace():
            for boundPackageID in earlyPackage.boundList:
                tempBoundPackage = self.packageTable.packages[self.packageTable.searchById(boundPackageID)]
                selectedTruck.loadPackage(tempBoundPackage)
                selectedTruck.currentAddress = tempBoundPackage.address + ' ' + tempBoundPackage.Zip
            selectedTruck.packageSort(self)

    # gets the report info from log and prints it to console
    def report(self, reportTime):
        try:
            reportTime = datetime.strptime(reportTime, '%H:%M').time()
            print(reportTime)
            lines = []
            with open('scanLog.txt', 'r') as log:
                lines = log.readlines()
            for line in lines:
                spaceOne = line.index(" ")
                spaceTwo = line.index(" ", spaceOne + 1)
                currentID = int(line[0: spaceOne])
                currentPackage = self.packageTable.packages[self.packageTable.searchById(currentID)]
                scanTime = line[spaceOne: spaceTwo].strip()
                scanTime = datetime.strptime(scanTime, '%I:%M').time()
                if scanTime <= reportTime:
                    currentPackage.status = line[spaceOne:].strip("\n")
            self.packageTable._print()
        except:
            print("Enter report time as  XX:XX")

    # used to indicate that the package has yet to arrive
    def lateScan(self, ID):
        with open('scanLog.txt', 'a') as log:
            currentPackage = self.packageTable.packages[self.packageTable.searchById(ID)]
            log.write(str(currentPackage.id) + ' ' + currentPackage.status + ' ' + "Scanned By Unknown\n")

    # starts report mode where you can enter a time and get package status at time
    def enterReportMode(self):
        reportTime = input("Enter report time type end to stop: \n")
        while reportTime != "end" and reportTime != "stop":
            self.report(reportTime)
            print(reportTime)
            reportTime = input("Enter report time type end to stop format time XX:XX \n")

    # used to look up package status by id
    def enterPackageLookup(self):
        with open('scanLog.txt', 'r') as log:
            lines = log.readlines()
        for line in lines:
            spaceOne = line.index(" ")
            currentID = int(line[0: spaceOne])
            currentPackage = self.packageTable.packages[self.packageTable.searchById(currentID)]
            currentPackage.status = line[spaceOne:].strip("\n")
        packageID = input("Enter package ID type end to stop: \n")
        while packageID != "end" and packageID != "stop":
            currentPackage = self.packageTable.packages[self.packageTable.searchById(packageID)]
            print(
                str(currentPackage.id) + currentPackage.status + " " + currentPackage.getShippingAddress() + " " + currentPackage.City + " Address" + str(
                    currentPackage.DeliveryDeadline) + " Deadline " + currentPackage.weight + " KILO")
            packageID = input("Enter package ID type end to stop: \n")
