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
print(Dispatch.findNextAddress('HUB',Dispatch.packageTable.packages))
input()
