from classes.package import package
from classes.hashTable import hashTbl
c1 = package()
print(c1.id)
c1.id = 0
print(c1.id)
hashTbl.passtest(c1)
print(c1.id)
c0 = hashTbl(10)
c0.add(c1)
c3 = package()
c3.id = 5
c4 = package()
c4.id = 15
c0.add(c3)
c0.add(c4)
print(c0.size)
c0._print()
c5 = c0.HashRemove(5)
c0._print()
c5._print()
input()
