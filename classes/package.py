from os import set_inheritable


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
    def _print(self):
        print(self.id, end='')

    def getShippingAddress(self):
        shippingaddress = self.address + ' '
        shippingaddress += self.Zip 
        return shippingaddress