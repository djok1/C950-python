from classes.package import package
from classes.hashTable import hashTbl
from classes.dispatch import dispatch
import csv
Dispatch = dispatch()
Dispatch.loadAddresses()
Dispatch.loadPackages()
print(Dispatch.getDistance(' HUB',' HUB'))
input()