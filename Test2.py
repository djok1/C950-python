from classes.package import package
from classes.hashTable import hashTbl
import csv
packagelist = []
with open('WGUPSPackageFile.csv', newline='') as csvfile:
    packagereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in packagereader:
        packagelist.append(row)
    for row in packagelist:
        print(row)
packageTable = hashTbl(len(packagelist))
for row in packagelist:
    tempPackage = package()
    tempPackage.id = int(row[0])
    tempPackage.address = row[1]
    tempPackage.City = row[2]
    tempPackage.State = row[3]
    tempPackage.Zip = row[4]
    tempPackage.DeliveryDeadline = row[5]
    tempPackage.SpecialNotes = row[7]
    packageTable.add(tempPackage)


packageTable._print()
input()