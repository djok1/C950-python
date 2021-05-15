from classes.package import package
from classes.hashTable import hashTbl
c1 = package()
print(c1.id)
c1.id = 0
print(c1.id)
hashTbl.passtest(c1)
print(c1.id)
c2 = hashTbl(10)
c2.add(c1)
c3 = package()
c3.id = 5
c4 = package()
c4.id = 15
c2.add(c3)
c2.add(c4)
print(c2.size)
print(c2.map)
input()
