# Packages.py
# initializing data and adding print method to display info
class Packages:
    def __init__(self, ID, address, city, state, zip, deadline, weight, notes, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.initialTime = None
        self.deliveredTime = None

    # Print information, only include delivery time if status is delivered
    def __str__(self):
        if self.status == "Delivered":
            return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.notes, self.status, self.deliveredTime)
        else:
            return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.notes, self.status)

    # Method that ensures that status is updated correctly when displayed to user.
    def status_update(self, time):
        if self.deliveredTime < time:
            self.status = "Delivered"
        elif self.initialTime < time:
            self.status = "En route"
        else:
            self.status = "At Hub"
