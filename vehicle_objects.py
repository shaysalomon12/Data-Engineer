# Importing an entire module
import Vehicle

# Or import classes Vehicle, ElectricVehicle from Vehicle.py file 
from Vehicle import Vehicle, ElectricVehicle


# Constructing an object
vehicle_object = Vehicle('Honda', 'Ridgeline', 'Truck')

print('--- Using classes ---')        
# Accessing attribute values
print(vehicle_object.brand)
print(vehicle_object.model)
print(vehicle_object.type)

# Calling methods
vehicle_object.fuel_up()
vehicle_object.drive()

# Creating multiple objects
vehicle_object = Vehicle('Honda', 'Ridgeline', 'Truck')
a_subaru = Vehicle('Subaru', 'Forester', 'Crossover')
an_suv = Vehicle('Ford', 'Explorer', 'SUV')

# Print an_suv object attributes 
print(an_suv.brand)
print(an_suv.model)
print(an_suv.type)

# Modifying an attribute directly
cool_new_vehicle = Vehicle('Honda', 'Ridgeline', 'Truck')
cool_new_vehicle.fuel_level = 7

# Print fuel level for "Honda Ridgeline Truck"
print(f'Fuel level for {cool_new_vehicle.brand} is {cool_new_vehicle.fuel_level}')

# Using child and parent methods
electric_vehicle = ElectricVehicle('Tesla', 'Model 3', 'Car')
electric_vehicle.charge()
electric_vehicle.drive()

# A collection of rental vehicles 
print('--- A collection of rental vehicles ---')

gas_fleet = []
electric_fleet = []

for i in range(100):
    vehicle = Vehicle('Honda', 'Civic', 'Car')
    gas_fleet.append(vehicle)

for j in range(50):
    evehicle = ElectricVehicle('Nissan', 'Leaf', 'Car')
    electric_fleet.append(evehicle)

for vehicle in gas_fleet:
    # print(vehicle)
    vehicle.fuel_up()

for evehicle in electric_fleet:
    # print(evehicle)
    evehicle.charge()

print(f'Gas vehicles: {len(gas_fleet)}')
print(f'Electric vehicles: {len(electric_fleet)}')

print('Gas vehicles:')
print(gas_fleet)

print('Electric vehicles:')
print(electric_fleet)

