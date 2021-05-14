from classes.package import package
from classes.hashTable import hashTbl
c1 = package()
print(c1.id)
c1.id = 0
print(c1.id)
hashTbl.passtest(c1)
print(c1.id)
c2 = hashTbl(1)
print(c2.size)
print(c2.map)
input()
