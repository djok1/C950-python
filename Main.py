# Dillon Odell 000958532
from classes.dispatch import dispatch

Dispatch = dispatch()
Dispatch.resetScanLog()
Dispatch.loadAddresses()
Dispatch.loadPackages()
Dispatch.loadBound(Dispatch.Trucks[1])
while not Dispatch.packageTable.allDelivered:
    Dispatch.loadTruck()
    for truck in Dispatch.Trucks:
        truck.deliverLoad(Dispatch)
    Dispatch.checkReturned()
Dispatch.loadTruck()
for truck in Dispatch.Trucks:
    truck.deliverLoad(Dispatch)
totalMiles = 0.0
for truck in Dispatch.Trucks:
    totalMiles += truck.miles
    print(str("{:.2f}".format(truck.miles)) + " truck " + str(truck.id) + " miles")
print(str("{:.2f}".format(totalMiles)) + " total miles")
# used to allow the user to select the mode
selection = input("Enter 0 for time report enter 1 to lookup by id type end to stop: \n")
while selection != "end" and selection != "stop":
    if selection == "0":
        Dispatch.enterReportMode()
    if selection == "1":
        Dispatch.enterPackageLookup()
    selection = input("Enter 0 for time report enter 1 to lookup by id type end to stop: \n")

# other possible algo edge vertex graph(dijkstra nearest n) Greedy algorithm
