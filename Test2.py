from classes.package import package
from classes.hashTable import hashTbl
from classes.dispatch import dispatch
import csv
Dispatch = dispatch()
Dispatch.resetScanLog()
Dispatch.loadAddresses()
Dispatch.loadPackages()
address0 = Dispatch.packageTable.packages[0].address + ' '
address0 += Dispatch.packageTable.packages[0].Zip
address1 = Dispatch.packageTable.packages[1].address + ' '
address1 += Dispatch.packageTable.packages[1].Zip
print(Dispatch.getDistance(address0,address1))
test = Dispatch.addressDic
print(Dispatch.Clock)
print(Dispatch.findNextPackage('HUB',Dispatch.packageTable.packages).address)
Dispatch.prioPackageList.add(Dispatch.packageTable.packages[0])
Dispatch.prioPackageList.add(Dispatch.packageTable.packages[2])
Dispatch.prioPackageList.add(Dispatch.packageTable.packages[4])
Dispatch.prioPackageList.HashRemove(Dispatch.packageTable.packages[2].id)
print(Dispatch.findNextPackage('HUB',Dispatch.prioPackageList.packages).address)
Dispatch.loadTruck()
for truck in Dispatch.Trucks:
    print("truck " + str(truck.id))
    for package in truck.packages:
        if package != None:
            print(str(package.id) + ' ' + package.status + ' ' + package.address + ' ' + package.Zip)
input()
