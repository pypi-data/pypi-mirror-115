import pytest
from src.trafficlight_statemachine import State, Green, Red, Yellow, ErrorState, TrafficLight

def test_base_state():
    '''This should test that the base class is abstract and trying to instantiate it yields an error with known message.'''
    with pytest.raises(Exception) as exc_info:
        state = State()  #   This should raise an exception
    exception_raised = exc_info.value
    assert type(TypeError()) == type(exception_raised)
    assert "Can't instantiate abstract class State with abstract methods on_event" in str(exc_info.__dict__)

def test_base_state_abstractmethod():
    '''This should test that the base class method.'''
    with pytest.raises(Exception) as exc_info:
        class TestState(State):     # creating an otherwise valid state (not the abc class but a child) without on_event()
            pass
        state = TestState()  #   This should raise an exception 
    exception_raised = exc_info.value
    assert type(TypeError()) == type(exception_raised)
    assert "Can't instantiate abstract class TestState with abstract methods on_event" in str(exc_info.__dict__)

def test_red_state_type():
    '''This tests the red state. Expectation: It should be a State--Red type.'''
    state = Red()
    assert type(Red()) == type(state)

def test_yellow_state_type():
    '''This tests the red state. Expectation: It should be a State--Yellow type.'''
    state = Yellow()
    assert type(Yellow()) == type(state)

def test_green_state_type():
    '''This tests the red state. Expectation: It should be a State--Green type.'''
    state = Green()
    assert type(Green()) == type(state)

def test_error_state_type():
    '''This tests the error state. Expectation: It should be a State--Error type.'''
    state = ErrorState()
    assert type(ErrorState()) == type(state)

def test_machine_init():
    '''This tests that the machine initializes correctly and has the right type'''
    machine = TrafficLight()
    assert type(TrafficLight()) == type(machine) 
    assert type(Red()) == type(machine.state)

def test_transitions_red_toGreen():
    '''This tests the state machine transitions correctly.'''
    machine = TrafficLight()
    assert type(TrafficLight()) == type(machine) 
    assert type(Red()) == type(machine.state) 
    machine.on_event("change")
    assert type(Green()) == type(machine.state)         # red to green

def test_transitions_red_toError():
    '''This tests the state machine transitions correctly.'''
    machine = TrafficLight()
    assert type(TrafficLight()) == type(machine) 
    assert type(Red()) == type(machine.state) 
    machine.on_event("bad input")
    assert type(ErrorState()) == type(machine.state)    # red to error

def test_transitions_error_toError():
    '''This tests the state machine transitions correctly (to error state with bad input and from error--> error with bad input).'''
    machine = TrafficLight()
    assert type(TrafficLight()) == type(machine) 
    assert type(Red()) == type(machine.state) 
    machine.on_event("bad input")
    assert type(ErrorState()) == type(machine.state)    # red to error
    machine.on_event("bad input")
    assert type(ErrorState()) == type(machine.state)    # error to error with bad input

def test_transitions_error_to_Red():
    '''This tests the state machine transitions correctly (to error state with bad input and from error--> error with bad input).'''
    machine = TrafficLight()
    assert type(TrafficLight()) == type(machine) 
    assert type(Red()) == type(machine.state) 
    machine.on_event("bad input")
    assert type(ErrorState()) == type(machine.state)    # red to error
    machine.on_event("change")
    assert type(Red()) == type(machine.state) 

def test_transitions_green_toYellow():
    '''This tests the state machine transitions correctly.'''
    machine = TrafficLight()
    assert type(TrafficLight()) == type(machine) 
    assert type(Red()) == type(machine.state) 
    machine.on_event("change")
    assert type(Green()) == type(machine.state)         # red to green
    machine.on_event("change")
    assert type(Yellow()) == type(machine.state)        # green to yellow

def test_transitions_green_toError():
    '''This tests the state machine transitions correctly.'''
    machine = TrafficLight()
    assert type(TrafficLight()) == type(machine) 
    assert type(Red()) == type(machine.state) 
    machine.on_event("change")
    assert type(Green()) == type(machine.state)         # red to green
    machine.on_event("bad input")
    assert type(ErrorState()) == type(machine.state)    # green to error

def test_transitions_yellow_toRed():
    '''This tests the state machine transitions correctly.'''
    machine = TrafficLight()
    assert type(TrafficLight()) == type(machine) 
    assert type(Red()) == type(machine.state) 
    machine.on_event("change")
    assert type(Green()) == type(machine.state)         # red to green
    machine.on_event("change")
    assert type(Yellow()) == type(machine.state)        # green to yellow
    machine.on_event("change")
    assert type(Red()) == type(machine.state)           # yellow back to red

def test_transitions_yellow_toError():
    '''This tests the state machine transitions correctly.'''
    machine = TrafficLight()
    assert type(TrafficLight()) == type(machine) 
    assert type(Red()) == type(machine.state) 
    machine.on_event("change")
    assert type(Green()) == type(machine.state)         # red to green
    machine.on_event("change")
    assert type(Yellow()) == type(machine.state)        # green to yellow
    machine.on_event("bad input")
    assert type(ErrorState()) == type(machine.state)    # yellow to error

def test_errorstate_on_event():
    '''This tests the state machine transitions correctly.'''
    machine = TrafficLight()
    assert type(TrafficLight()) == type(machine) 
    assert type(Red()) == type(machine.state) 
    machine.on_event(42)    #invalid data
    assert type(ErrorState()) == type(machine.state)    # should be error

def test_repr_redstate():
    state = Red()
    assert "Red" == repr(state) 

def test_str_redstate():
    state = Red()
    assert "Red" == str(state)

def test_repr_yellowstate():
    state = Yellow()
    assert "Yellow" == repr(state) 

def test_str_yellowstate():
    state = Yellow()
    assert "Yellow" == str(state)

def test_repr_greenstate():
    state = Green()
    assert "Green" == repr(state) 

def test_str_greenstate():
    state = Green()
    assert "Green" == str(state)

def test_repr_errorstate():
    state = ErrorState()
    assert "ErrorState" == repr(state) 

def test_str_errorstate():
    state = ErrorState()
    assert "ErrorState" == str(state)