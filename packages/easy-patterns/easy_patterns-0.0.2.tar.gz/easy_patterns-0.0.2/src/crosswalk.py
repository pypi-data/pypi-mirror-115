import typing
from car_statemachine import Car
from trafficlight_statemachine import TrafficLight
import time

def printlines(num_lines:int):
    '''This just prints a predefined number of lines to clear a terminal screen between printing chunks of text.'''
    for x in range(0, num_lines):
        print()

def printgreenlight():
    '''This prints an ASCII simulation of a green light.'''
    green = '''
                                      "GREEN LIGHT!"

                                        i-------i
                                        i       i
                                        i_______i
                                        i-------i
                                        i       i
                                        i_______i
                                        i-------i
                                        i XXXXX i
                                        i_______i                                        
'''
    printlines(20)
    print(green)

def printredlight():
    '''This prints an ASCII simulation of a red light.'''
    red = '''
                                       "RED LIGHT!"

                                        i-------i
                                        i XXXXX i
                                        i_______i
                                        i-------i
                                        i       i
                                        i_______i
                                        i-------i
                                        i       i
                                        i_______i                                        
'''
    printlines(20)
    print(red)

def printyellowlight():
    '''This prints an ASCII simulation of a yellow light.'''
    yellow = '''
                                      "YELLOW LIGHT!"

                                        i-------i
                                        i       i
                                        i_______i
                                        i-------i
                                        i XXXXX i
                                        i_______i
                                        i-------i
                                        i       i
                                        i_______i                                        
'''
    printlines(20)
    print(yellow)

def simulate_crosswalk():
    '''This is a simple simulation of a crosswalk to demonstrate the two state machines interacting.'''
    printlines(30)
    print("In a World . . .")
    time.sleep(3)
    printlines(30)
    print("Where pedestrians' only hope is a working signal light . . .")
    time.sleep(3)
    printlines(30)
    print("There is a street running East-West, and a crosswalk known as . . .")
    time.sleep(3)
    printlines(30)
    print("Dramatic pause . . .")
    time.sleep(3)
    printlines(30)
    print("The Crosswalk!")
    time.sleep(3)
    car1 = Car()
    light = TrafficLight()      # default starting state is red
    light.on_event("change")    # changing to green
    car1.on_event(light)
    printgreenlight()
    time.sleep(1)
    printlines(30)
    print(f"The car is {car1.state} as it heads for the crosswalk, beacuse the light is {light.state}.")
    time.sleep(3)
    light.on_event("change")    # changing to yellow
    car1.on_event(light)
    printyellowlight()
    time.sleep(1)
    printlines(30)
    print(f"The car is {car1.state} as it heads toward the crosswalk, because the light is {light.state}.")
    time.sleep(3)
    light.on_event("change")    # changing to red
    car1.on_event(light)
    printredlight()
    time.sleep(1)
    printlines(30)
    print(f"The car is {car1.state} as it heads toward the crosswalk, because the light is {light.state}.")
    print("Whew! Now the pedestrians can cross in peace and safety.")
    time.sleep(3)
    printlines(30)
    print("Hey, notice how none of this downstream code had to manage the state. Weird! Play with the objects yourself.")
    print("Call 'light = TrafficLight()' and 'car = Car()'.")
    print("Access the state of car with 'car.state' and the state of the light with 'light.state'.")
    print("You can then change the state of the light with 'light.on_event('change')'.")
    print("You can then change the car's state with 'car.on_event(light)'.")