# Classes

class Vehicle:
    def __init__(self, brand, model, type):
        self.brand = brand
        self.model = model
        self.type = type
        self.gas_tank_size = 14
        self.fuel_level = 0

    def fuel_up(self):
        self.fuel_level = self.gas_tank_size
        print('Gas tank is now full.')

    def drive(self):
        print(f'The {self.model} is now driving.')

    def update_fuel_level(self, new_level):
        if new_level <= self.gas_tank_size:
            self.fuel_level = new_level
        else:
            print('Exceeded capacity')

    def get_gas(self, amount):
        if (self.fuel_level + amount <= self.gas_tank_size):
            self.fuel_level += amount
            print('Added fuel.')
        else:
            print('The tank wont hold that much.')
 
class ElectricVehicle(Vehicle):
    def __init__(self, brand, model, type):
        super().__init__(brand, model, type)
        self.battery_size = 85
        self.charge_level = 0

    def charge(self):
        self.charge_level = 100
        print('The vehicle is now charged.')

    def fuel_up(self):
        print('This vehicle has no fuel tank!')
 

class Battery:
    def __init__(self, size=85):
        self.size = size
        self.charge_level = 0

    def get_range(self):
        if self.size == 85:
            return 260
        elif self.size == 100:
            return 315
