#   States: 
# This file is where the actual states go. This is simple to keep the demonstrator fairly easy to grok.
# The states for the traffic light are red, yellow, and green.

from abc import ABC, abstractmethod     # this is not absolutely necessary, but it helps enforce discipline making states
import typing                           # also not absolutely necessary, but typing gives clues re types
import time

class State(ABC):
    '''This is the base class for a state. Each state holds the logic of when to transition to the next.'''
    def __init__(self):
        pass

    @abstractmethod
    def on_event(self, call_to_switch: str): 
        '''When it is necessary to switch, this takes the call_to_switch and directs the light to change states.'''

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

#------- These are the concrete states:------------------
class Red(State):
    '''This represents a trafficlight being red. When called upon to change, it should change to green. Else error.'''
    def on_event(self, call_to_switch:str): 
        if call_to_switch == "change":
            return Green()
        else:
            return ErrorState()

class Green(State):
    '''This represents a trafficlight being green. When called upon to change, it should change to yellow. Else error.'''
    def on_event(self, call_to_switch:str): 
        if call_to_switch == "change":
            return Yellow()
        else:
            return ErrorState()

class Yellow(State):
    '''This represents a trafficlight being yellow. When called upon to change, it should change to red. Else error.'''
    def on_event(self, call_to_switch:str): 
        if call_to_switch == "change":
            return Red()
        else:
            return ErrorState()

class ErrorState(State):
    '''This is the basic error state for the traffic light.'''
    def on_event(self, call_to_switch:str): 
        if call_to_switch == "change":
            return Red()
        else:
            return ErrorState()

#--------- The actual state machine itself:-----------------
class TrafficLight:             #   This is the actual Finite State Machine
    '''This is the state machine itself and this object can be called upon downstream to represent a traffic light that
    switches to different states when the "change" value is included in state.on_event() as a parameter.

    Call this in client code as such:
    from trafficlight_statemachine import TrafficLight
    light = TrafficLight()
    light.on_event("change")'''
    def __init__(self):
        self.state = Red() #  starting state is now set as red

    def on_event(self, call_to_switch:str):
        self.state = self.state.on_event(call_to_switch)