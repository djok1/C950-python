from copy import deepcopy

import classes.package


class hashTbl:
    def __init__(self, size):
        self.size = size
        self.packages = [False] * self.size
        self.allDelivered = False

    # retruns the hash code location based off of key(ID)
    def _get_hash(self, key):
        hash = int(key) % self.size
        return hash

    # Adds package to table
    def add(self, curentPackage):
        curentPackage.hash = self._get_hash(curentPackage.id)
        if self.packages[curentPackage.hash] == False or self.packages[curentPackage.hash] == -1:
            self.packages[curentPackage.hash] = curentPackage
        else:
            i = 1
            size = self.size - 1
            while i <= self.size:
                if i + curentPackage.hash > size:
                    if not (self.packages[i - curentPackage.hash]) or self.packages[i - curentPackage.hash] == -1:
                        self.packages[i - curentPackage.hash] = curentPackage
                        break
                else:
                    if not (self.packages[i + curentPackage.hash]) or self.packages[i + curentPackage.hash] == -1:
                        self.packages[i + curentPackage.hash] = curentPackage
                        break
                i += 1
            if i > self.size:
                self.adjustSize(curentPackage)

    # prints the package status
    def _print(self):
        i = 0
        print('Package Status')
        while i < self.size:
            if not (self.packages[i]) or self.packages[i] == -1:
                print(self.packages[i])
            else:
                print(str(self.packages[i].id) + self.packages[i].status + " " + self.packages[i].getShippingAddress()
                      + " " + self.packages[i].City + " Address" + str(self.packages[i].DeliveryDeadline) +
                      " Deadline " + self.packages[i].weight + " KILO")
            i += 1

    # removes the package by ID
    def HashRemove(self, id):
        location = self.searchById(id)
        remove = self.packages[location]
        self.packages[location] = -1

        return remove

    # returns the location of the ID
    def searchById(self, id):
        id = int(id)
        idHash = self._get_hash(id)
        i = 0
        size = self.size - 1

        while i <= self.size:
            if (i + idHash > size):
                if (self.packages[i - idHash] != -1 and self.packages[i - idHash].id == id):
                    return i - idHash
                    break
                elif (not (self.packages[i - idHash])):
                    break
            else:
                if (self.packages[i + idHash] != -1 and self.packages[i + idHash].id == id):
                    return i + idHash
                    break
                elif (not (self.packages[i - idHash])):
                    break

            i += 1
        print("id not found")
        return -1

    def adjustSize(self, curentPackage):
        temptable = deepcopy(self)
        self.size *= 2
        self.packages.clear()
        self.packages = [False] * self.size
        for package in temptable:
            self.add(package)
        self.add(curentPackage)
