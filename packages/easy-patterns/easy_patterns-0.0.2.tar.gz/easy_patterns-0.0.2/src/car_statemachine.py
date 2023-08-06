# The states for the car--"driving, coasting, and braking"--correspond to the traffic light states green, yellow, and red
from abc import ABC, abstractmethod     # this is not absolutely necessary, but it helps enforce discipline making states
import typing                           # also not absolutely necessary, but typing gives clues re types
import time

class CarState(ABC):
    '''This is the base class for a state. Each state holds the logic of when to transition to the next.'''
    def __init__(self):
        pass

    @abstractmethod
    def on_event(self, trafficlight:object): 
        '''When it is necessary to switch, this takes the call_to_switch and directs the light to change states.'''
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

#------- These are the concrete states:------------------
class Braking(CarState):
    '''This represents a car braking for a red light. When the light is green, the state should transition to driving. If it is yellow,
    the state should transition to Coasting. If the light input is Red, it should stay in Braking. Else error.    '''
    def on_event(self, trafficlight): 
        try:
            if str(trafficlight.state) == "Green":
                return Driving()
            if str(trafficlight.state) == "Yellow":
                return Coasting()
            if str(trafficlight.state) == "Red":
                return self
            else:
                return Car_ErrorState()
        except:
            return Car_ErrorState()

class Driving(CarState):
    '''This represents a car driving on a green light. When the light turns yellow, it should change to Coasting. If it is Red, the state should transition to
    Braking. If it is Green, the state should stay in driving state. Else error.'''
    def on_event(self, trafficlight): 
        try:
            if str(trafficlight.state) == "Yellow":
                return Coasting()
            if str(trafficlight.state) == "Red":
                return Braking()
            if str(trafficlight.state) == "Green":
                return self
            else:
                return Car_ErrorState()
        except:
            return Car_ErrorState()

class Coasting(CarState):
    '''This represents a car coasting for yellow light. When the light turns red, it should change to Braking. Else error.'''
    def on_event(self, trafficlight): 
        try:
            if str(trafficlight.state) == "Red":
                return Braking()
            if str(trafficlight.state) == "Green":
                return Driving()
            if str(trafficlight.state) == "Yellow":
                return self
            else:
                return Car_ErrorState()
        except:
            return Car_ErrorState()

class Car_ErrorState(CarState):
    '''This represents a car in an Error State--IE: a traffic light is either out or blinking red. If a normal input comes back, it transitions
    to one of the regular operating states.'''
    def on_event(self, trafficlight): 
        try:
            if str(trafficlight.state) == "Red":
                return Braking()
            if str(trafficlight.state) == "Yellow":
                return Coasting()
            if str(trafficlight.state) == "Green":
                return Driving()
            else:
                return self
        except:
            return self

#--------- The actual state machine itself:-----------------
class Car:             #   This is the actual Finite State Machine
    '''This is the state machine itself and this object can be called upon downstream to represent a car that
    switches to different states when the light does.

    Call this in client code as such:
    from trafficlight_statemachine import Car
    car = Car()
    car.on_event(trafficlight)'''
    def __init__(self):
        self.state = Braking() #  starting state is now set as braking

    def on_event(self, trafficlight):
        self.state = self.state.on_event(trafficlight)