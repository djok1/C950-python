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
    def _print(self):
        print(self.id, end='')

        