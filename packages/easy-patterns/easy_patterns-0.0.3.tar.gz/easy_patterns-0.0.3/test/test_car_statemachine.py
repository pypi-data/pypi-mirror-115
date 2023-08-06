import pytest
from src.car_statemachine import CarState, Braking, Driving, Coasting, Car_ErrorState, Car
from src.trafficlight_statemachine import Green, Red, Yellow, ErrorState, TrafficLight

def test_base_state_car():
    '''This should test that the base class is abstract and trying to instantiate it yields an error with known message.'''
    with pytest.raises(Exception) as exc_info:
        state = CarState()  #   This should raise an exception
    exception_raised = exc_info.value
    assert type(TypeError()) == type(exception_raised)
    assert "Can't instantiate abstract class CarState with abstract methods on_event" in str(exc_info.__dict__)

def test_base_state_abstractmethod_car():
    '''This should test that the instantiating a child of the base class without an abstract method fails.'''
    with pytest.raises(Exception) as exc_info:
        class TestState(CarState):
            pass
        state = TestState()  #   This should raise an exception because there is no implementation of the on_event method
    exception_raised = exc_info.value
    assert type(TypeError()) == type(exception_raised)
    assert "Can't instantiate abstract class TestState with abstract methods on_event" in str(exc_info.__dict__)

def test_braking_state_type():
    '''This tests the braking state. Expectation: It should be a State--Braking type with str "Braking.'''
    state = Braking()
    assert type(Braking()) == type(state)
    assert "Braking" == str(state)
    assert "Braking" == repr(state)

def test_driving_state_type():
    '''This tests the driving state. Expectation: It should be a State--Driving type and its str should be "Driving".'''
    state = Driving()
    assert type(Driving()) == type(state)
    assert "Driving" == str(state)
    assert "Driving" == repr(state)

def test_coasting_state_type():
    '''This tests the coasting state. Expectation: It should be a State--Coasting type with an str value of "Coasting".'''
    state = Coasting()
    assert type(Coasting()) == type(state)
    assert "Coasting" == str(state)
    assert "Coasting" == repr(state)

def test_error_state_type():
    '''This tests the error state. Expectation: It should be a State--Car_ErrorState type and the str should be "Car_ErrorState.'''
    state = Car_ErrorState()
    assert type(Car_ErrorState()) == type(state)
    assert "Car_ErrorState" == str(state)
    assert "Car_ErrorState" == repr(state)

def test_braking_transition_green():
    '''This tests the braking transition logic with a valid light state as a parameter (green-->driving).'''
    state = Braking()
    light = TrafficLight()
    light.on_event("change")    # red to green
    new_state = state.on_event(light)
    assert "Driving" == str(new_state)

def test_braking_transition_yellow():
    '''This tests the braking transition logic with a valid light state as a parameter (yellow-->coasting).'''
    state = Braking()
    light = TrafficLight()
    light.on_event("change")    # red to green
    light.on_event("change")    # to yellow
    new_state = state.on_event(light)
    assert "Coasting" == str(new_state)

def test_braking_transition_red():
    '''This tests the braking transition logic with a valid light state as a parameter (red-->braking).'''
    state = Braking()
    light = TrafficLight()
    light.on_event("change")    # red to green
    light.on_event("change")    # to yellow
    light.on_event("change")    # to red
    new_state = state.on_event(light)
    assert "Braking" == str(new_state)

def test_braking_transition_error():
    '''This tests the braking transition logic with a light in the error state (ErrorState-->Car_ErrorState).'''
    state = Braking()
    light = TrafficLight()
    light.on_event("change")        # red to green
    light.on_event("change")        # to yellow
    light.on_event("bad input")     # to ErrorState
    new_state = state.on_event(light)
    assert "Car_ErrorState" == str(new_state)

def test_braking_transition_bad_input():
    '''This tests the braking transition logic with a light in the error state (ErrorState-->Car_ErrorState).'''
    state = Braking()
    light = TrafficLight()
    new_state = state.on_event("bad data to car")
    assert "Car_ErrorState" == str(new_state)

def test_coasting_transition_green():
    '''This tests the coasting transition logic with a valid light state as a parameter (green-->driving).'''
    state = Coasting()
    light = TrafficLight()
    light.on_event("change")    # red to green
    new_state = state.on_event(light)
    assert "Driving" == str(new_state)

def test_coasting_transition_yellow():
    '''This tests the coasting transition logic with a valid light state as a parameter (yellow-->coasting).'''
    state = Coasting()
    light = TrafficLight()
    light.on_event("change")    # red to green
    light.on_event("change")    # to yellow
    new_state = state.on_event(light)
    assert "Coasting" == str(new_state)

def test_coasting_transition_red():
    '''This tests the coasting transition logic with a valid light state as a parameter (red-->braking).'''
    state = Coasting()
    light = TrafficLight()
    light.on_event("change")    # red to green
    light.on_event("change")    # to yellow
    light.on_event("change")    # to red
    new_state = state.on_event(light)
    assert "Braking" == str(new_state)

def test_coasting_transition_error():
    '''This tests the coasting transition logic with a light in the error state (ErrorState-->Car_ErrorState).'''
    state = Coasting()
    light = TrafficLight()
    light.on_event("change")        # red to green
    light.on_event("change")        # to yellow
    light.on_event("bad input")     # to ErrorState
    new_state = state.on_event(light)
    assert "Car_ErrorState" == str(new_state)

def test_coasting_transition_bad_input():
    '''This tests the coasting transition logic with invalid data.'''
    state = Coasting()
    new_state = state.on_event("invalid data to car")
    assert "Car_ErrorState" == str(new_state)    

def test_driving_transition_green():
    '''This tests the driving transition logic with a valid light state as a parameter (green-->driving).'''
    state = Driving()
    light = TrafficLight()
    light.on_event("change")    # red to green
    new_state = state.on_event(light)
    assert "Driving" == str(new_state)

def test_driving_transition_yellow():
    '''This tests the driving transition logic with a valid light state as a parameter (yellow-->coasting).'''
    state = Driving()
    light = TrafficLight()
    light.on_event("change")    # red to green
    light.on_event("change")    # to yellow
    new_state = state.on_event(light)
    assert "Coasting" == str(new_state)

def test_driving_transition_red():
    '''This tests the driving transition logic with a valid light state as a parameter (red-->braking).'''
    state = Driving()
    light = TrafficLight()
    light.on_event("change")    # red to green
    light.on_event("change")    # to yellow
    light.on_event("change")    # to red
    new_state = state.on_event(light)
    assert "Braking" == str(new_state)

def test_driving_transition_error():
    '''This tests the driving transition logic with a light in the error state (ErrorState-->Car_ErrorState).'''
    state = Driving()
    light = TrafficLight()
    light.on_event("change")        # red to green
    light.on_event("change")        # to yellow
    light.on_event("bad input")     # to ErrorState
    new_state = state.on_event(light)
    assert "Car_ErrorState" == str(new_state)

def test_driving_transition_bad_input():
    '''This tests the driving transition logic with invalid data.'''
    state = Driving()
    new_state = state.on_event("invalid data to car")
    assert "Car_ErrorState" == str(new_state)    

def test_error_transition_green():
    '''This tests the Car_ErrorState transition logic with a valid light state as a parameter (green-->driving).'''
    state = Car_ErrorState()
    light = TrafficLight()
    light.on_event("change")    # red to green
    new_state = state.on_event(light)
    assert "Driving" == str(new_state)

def test_error_transition_yellow():
    '''This tests the Car_ErrorState transition logic with a valid light state as a parameter (yellow-->coasting).'''
    state = Car_ErrorState()
    light = TrafficLight()
    light.on_event("change")    # red to green
    light.on_event("change")    # to yellow
    new_state = state.on_event(light)
    assert "Coasting" == str(new_state)

def test_error_transition_red():
    '''This tests the Car_ErrorState transition logic with a valid light state as a parameter (red-->braking).'''
    state = Car_ErrorState()
    light = TrafficLight()
    light.on_event("change")    # red to green
    light.on_event("change")    # to yellow
    light.on_event("change")    # to red
    new_state = state.on_event(light)
    assert "Braking" == str(new_state)

def test_error_transition_error():
    '''This tests the coasting transition logic with a light in the error state (ErrorState-->Car_ErrorState).'''
    state = Car_ErrorState()
    light = TrafficLight()
    light.on_event("change")        # red to green
    light.on_event("change")        # to yellow
    light.on_event("bad input")     # to ErrorState
    new_state = state.on_event(light)
    assert "Car_ErrorState" == str(new_state)

def test_error_transition_bad_input():
    '''This tests the coasting transition logic with invalid data.'''
    state = Car_ErrorState()
    new_state = state.on_event("invalid data to car")
    assert "Car_ErrorState" == str(new_state)    

def test_transition_car_braking_to_driving():
    '''This tests the transitions with a car from braking to driving.'''
    car = Car()
    light = TrafficLight()
    assert type(Braking()) == type(car.state)
    assert type(Red()) == type(light.state)
    light.on_event("change")
    car.on_event(light)
    assert type(Driving()) == type(car.state)
    assert type(Green()) == type(light.state)

def test_transition_car_braking_to_coasting():
    '''This tests the transitions with a car from braking to coasting.'''
    car = Car()
    light = TrafficLight()
    assert type(Braking()) == type(car.state)
    assert type(Red()) == type(light.state)
    light.on_event("change")
    light.on_event("change")
    car.on_event(light)
    assert type(Coasting()) == type(car.state)
    assert type(Yellow()) == type(light.state)

def test_transition_car_braking_to_braking():
    '''This tests the transitions with a car from braking to braking.'''
    car = Car()
    light = TrafficLight()
    assert type(Braking()) == type(car.state)
    assert type(Red()) == type(light.state)
    car.on_event(light)
    assert type(Braking()) == type(car.state)
    assert type(Red()) == type(light.state)

def test_transition_car_braking_to_error_bad_light_state():
    '''This tests the transitions with a car from braking to Car_ErrorState due to a light in ErrorState.'''
    car = Car()
    light = TrafficLight()
    light.on_event("bad input for light")
    car.on_event(light)
    assert type(Car_ErrorState()) == type(car.state)
    assert type(ErrorState()) == type(light.state)

def test_transition_car_braking_to_error_bad_car_state():
    '''This tests the transitions with a car from braking to Car_ErrorState due to invalid input for the car.'''
    car = Car()
    light = TrafficLight()
    assert type(Braking()) == type(car.state)
    assert type(Red()) == type(light.state)
    car.on_event(light)     #car is braking
    assert type(Braking()) == type(car.state)
    car.on_event("bad data creating error")
    assert type(Car_ErrorState()) == type(car.state)

def test_transition_car_driving_to_driving():
    '''This tests the transitions with a car from driving to driving.'''
    car = Car()
    light = TrafficLight()
    light.on_event("change")        #   green
    car.on_event(light)
    assert type(Driving()) == type(car.state)
    assert type(Green()) == type(light.state)
    car.on_event(light)
    assert type(Driving()) == type(car.state)
    assert type(Green()) == type(light.state)

def test_transition_car_driving_to_coasting():
    '''This tests the transitions with a car from driving to coasting.'''
    car = Car()
    light = TrafficLight()
    light.on_event("change")        #   green
    car.on_event(light)
    assert type(Driving()) == type(car.state)
    assert type(Green()) == type(light.state)
    light.on_event("change")        #   yellow
    car.on_event(light)
    assert type(Coasting()) == type(car.state)
    assert type(Yellow()) == type(light.state)

def test_transition_car_driving_to_braking():
    '''This tests the transitions with a car from driving to braking.'''
    car = Car()
    light = TrafficLight()
    light.on_event("change")        #   green
    car.on_event(light)
    assert type(Driving()) == type(car.state)
    assert type(Green()) == type(light.state)
    light.on_event("change")        #   yellow
    light.on_event("change")        #   red
    car.on_event(light)
    assert type(Braking()) == type(car.state)
    assert type(Red()) == type(light.state)

def test_transition_car_driving_to_error_bad_light_state():
    '''This tests the transitions with a car from driving to Car_ErrorState due to a light in ErrorState.'''
    car = Car()
    light = TrafficLight()
    light.on_event("change")        #   green
    car.on_event(light)
    assert type(Driving()) == type(car.state)   #now driving
    assert type(Green()) == type(light.state)
    light.on_event("bad input for light")
    car.on_event(light)
    assert type(Car_ErrorState()) == type(car.state)
    assert type(ErrorState()) == type(light.state)

def test_transition_car_driving_to_error_bad_car_state():
    '''This tests the transitions with a car from driving to Car_ErrorState due to invalid input for the car.'''
    car = Car()
    light = TrafficLight()
    light.on_event("change")        #   green
    car.on_event(light)
    assert type(Driving()) == type(car.state)   #now driving
    assert type(Green()) == type(light.state)
    car.on_event("bad data creating error")
    assert type(Car_ErrorState()) == type(car.state)


def test_transition_car_coasting_to_driving():
    '''This tests the transitions with a car from coasting to driving.'''
    car = Car()
    light = TrafficLight()
    light.on_event("change")        #   green
    light.on_event("change")        #   yellow
    car.on_event(light)
    assert type(Coasting()) == type(car.state)
    assert type(Yellow()) == type(light.state)
    light.on_event("change")        #   red
    light.on_event("change")        #   green
    car.on_event(light)
    assert type(Driving()) == type(car.state)
    assert type(Green()) == type(light.state)

def test_transition_car_coasting_to_coasting():
    '''This tests the transitions with a car from coasting to coasting.'''
    car = Car()
    light = TrafficLight()
    light.on_event("change")        #   green
    light.on_event("change")        #   yellow
    car.on_event(light)
    assert type(Coasting()) == type(car.state)
    assert type(Yellow()) == type(light.state)
    car.on_event(light)
    assert type(Coasting()) == type(car.state)
    assert type(Yellow()) == type(light.state)

def test_transition_car_coasting_to_braking():
    '''This tests the transitions with a car from coasting to braking.'''
    car = Car()
    light = TrafficLight()
    light.on_event("change")        #   green
    light.on_event("change")        #   yellow
    car.on_event(light)
    assert type(Coasting()) == type(car.state)
    assert type(Yellow()) == type(light.state)
    light.on_event("change")        #   red
    car.on_event(light)
    assert type(Braking()) == type(car.state)
    assert type(Red()) == type(light.state)

def test_transition_car_coasting_to_error_bad_light_state():
    '''This tests the transitions with a car from coasting to Car_ErrorState due to a light in ErrorState.'''
    car = Car()
    light = TrafficLight()
    light.on_event("change")        #   green
    light.on_event("change")        #   yellow
    car.on_event(light)
    assert type(Coasting()) == type(car.state)
    assert type(Yellow()) == type(light.state)
    light.on_event("bad input for light")
    car.on_event(light)
    assert type(Car_ErrorState()) == type(car.state)
    assert type(ErrorState()) == type(light.state)

def test_transition_car_coasting_to_error_bad_car_state():
    '''This tests the transitions with a car from coasting to Car_ErrorState due to invalid input for the car.'''
    car = Car()
    light = TrafficLight()
    light.on_event("change")        #   green
    light.on_event("change")        #   yellow
    car.on_event(light)
    assert type(Coasting()) == type(car.state)
    assert type(Yellow()) == type(light.state)
    car.on_event("bad data creating error")
    assert type(Car_ErrorState()) == type(car.state)

def test_transition_car_error_to_driving():
    '''This tests the transitions with a car from error to driving.'''
    car = Car()
    light = TrafficLight()
    car.on_event("throwing error")
    light.on_event("change")        #   green
    car.on_event(light)
    assert type(Driving()) == type(car.state)
    assert type(Green()) == type(light.state)

def test_transition_car_error_to_coasting():
    '''This tests the transitions with a car from error to coasting.'''
    car = Car()
    light = TrafficLight()
    car.on_event("throwing error")
    light.on_event("change")        #   green
    light.on_event("change")        #   yellow
    car.on_event(light)
    assert type(Coasting()) == type(car.state)
    assert type(Yellow()) == type(light.state)

def test_transition_car_error_to_braking():
    '''This tests the transitions with a car from error to braking.'''
    car = Car()
    light = TrafficLight()
    car.on_event("throwing error")
    car.on_event(light)
    assert type(Braking()) == type(car.state)
    assert type(Red()) == type(light.state)

def test_transition_car_coasting_to_error_bad_light_state():
    '''This tests the transitions with a car from error to Car_ErrorState due to a light in ErrorState.'''
    car = Car()
    light = TrafficLight()
    car.on_event("throwing error")
    assert type(Car_ErrorState()) == type(car.state)
    light.on_event("bad input for light")
    car.on_event(light)
    assert type(Car_ErrorState()) == type(car.state)
    assert type(ErrorState()) == type(light.state)

def test_transition_car_coasting_to_error_bad_car_state():
    '''This tests the transitions with a car from coasting to Car_ErrorState due to invalid input for the car.'''
    car = Car()
    light = TrafficLight()
    car.on_event("throwing error")
    assert type(Car_ErrorState()) == type(car.state)    
    car.on_event("bad data creating error")
    assert type(Car_ErrorState()) == type(car.state)    

##############################################################################################################################

