from datetime import time

class truck:
    size = 16
    Clock = time(hour = 8)
    def __init__(self,id):
        self.id = id
        self.packages = [False] * self.size

    def scan(self, table, id, scanType):
        table.packages[table.searchById(id)].status = scanType + " " + self.Clock
        with open('scanLog.txt', 'w') as log:
            log.write(table.searchById(id).status)
    