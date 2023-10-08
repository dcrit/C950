import datetime
class Package:
    def __init__(self, ID, address, city, state, zip, deadline, weight, status, delivery_time):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zip,
                                                       self.deadline, self.weight, self.status, self.delivery_time)
