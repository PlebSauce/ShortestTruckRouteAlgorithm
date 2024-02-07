# Truck.py
# initializing data and adding print method to display info
class Truck:
    def __init__(self, packages, millage, currLocation, initialTime):
        self.packages = packages
        self.millage = millage
        self.currLocation = currLocation
        self.time = initialTime
        self.initialTime = initialTime

    def __str__(self):
        return "%s, %s, %s, %s" % (self.packages, self.millage, self.currLocation, self.time)
