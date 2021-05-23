from classes.package import package
from classes.hashTable import hashTbl
from classes.dispatch import dispatch
import csv
Dispatch = dispatch()
Dispatch.loadAddresses()
Dispatch.loadPackages()
address0 = Dispatch.packageTable.map[0].address + ' '
address0 += Dispatch.packageTable.map[0].Zip
address1 = Dispatch.packageTable.map[1].address + ' '
address1 += Dispatch.packageTable.map[1].Zip
print(Dispatch.getDistance(address0,address1))
test = Dispatch.addressDic
input()