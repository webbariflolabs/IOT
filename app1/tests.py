class Vehicle:

    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

class Bus(Vehicle):
    def display(self):
        print(self.name)

bus = Bus('Blue',100,10)
bus.display()
