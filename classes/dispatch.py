#import classes.truck
from classes.package import package
from classes.hashTable import hashTbl
from collections import defaultdict
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
        packageTable = hashTbl(len(packagelist))
        packageTable = hashTbl(len(packagelist))
        for row in packagelist:
            addressDic[row[1] + " " + row[4]].append(int(row[0]))
            tempPackage = package()
            tempPackage.id = int(row[0])
            tempPackage.address = row[1]
            tempPackage.City = row[2]
            tempPackage.State = row[3]
            tempPackage.Zip = row[4]
            tempPackage.DeliveryDeadline = row[5]
            tempPackage.SpecialNotes = row[7]
            packageTable.add(tempPackage)
        self.packageTable = packageTable
        self.addressDic = addressDic
    
    def getDistance(self,startLocation,endLocation):
        return self.Distancelist[startLocation][endLocation]

        