import typing
from car_statemachine import Car
from trafficlight_statemachine import TrafficLight
import time

def printlines(num_lines:int):
    '''This just prints a predefined number of lines to clear a terminal screen between printing chunks of text.'''
    for x in range(0, num_lines):
        print()

def simulate_crosswalk():
    '''This is a simple simulation of a crosswalk to demonstrate the two state machines interacting.'''
    printlines(20)
    print("In a World . . .")
    time.sleep(3)
    printlines(20)
    print("Where pedestrians' only hope is a working signal light . . .")
    time.sleep(3)
    printlines(20)
    print("There is a street running East-West, and a crosswalk known as . . .")
    time.sleep(3)
    printlines(20)
    print("Dramatic pause . . .")
    time.sleep(3)
    printlines(20)
    print("The Crosswalk!")
    time.sleep(3)
    car1 = Car()
    light = TrafficLight()      # default starting state is red
    light.on_event("change")    # changing to green
    car1.on_event(light)
    printlines(20)
    print(f"The car is {car1.state} as it heads for the crosswalk, beacuse the light is {light.state}.")
    time.sleep(3)
    light.on_event("change")    # changing to yellow
    car1.on_event(light)
    printlines(20)
    print(f"The car is {car1.state} as it heads toward the crosswalk, because the light is {light.state}.")
    time.sleep(3)
    light.on_event("change")    # changing to red
    car1.on_event(light)
    printlines(20)
    print(f"The car is {car1.state} as it heads toward the crosswalk, because the light is {light.state}.")
    printlines(20)
    time.sleep(3)
    print("Whew! Now the pedestrians can cross in peace and safety.")
    printlines(20)
    time.sleep(3)
    print("Hey, notice how none of this downstream code had to manage the state. Weird!")