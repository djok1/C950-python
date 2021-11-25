from os import set_inheritable
from datetime import time

time = time(hour=8)
priority = 0


class package:
    def __init__(self):
        self.id = -1
        self.address = None
        self.City = None
        self.State = None
        self.Zip = None
        self.DeliveryDeadline = None
        self.SpecialNotes = None
        self.status = "unknown"
        self.boundList = []
        self.truck = -1
        self.weight = 0

    # prints the ID of the package
    def _print(self):
        print(self.id, end='')

    # returns the shipping address
    def getShippingAddress(self):
        shippingaddress = self.address + ' '
        shippingaddress += self.Zip
        return shippingaddress
