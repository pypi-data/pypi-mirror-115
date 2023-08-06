# easy_patterns
Demonstrator for teaching design patterns in Python

__Using This Package:__
This package has the module crosswalk, with the principal function 'crosswalk.simulate_crosswalk()' for running two statemachines (Car and TrafficLight). 
It also has the state machines themselves and their respective states Car: [ CarState, Braking, Driving, Coasting, Car_ErrorState ], 
and TrafficLight: [ State, Red, Green, Yellow, ErrorState ]. Feel free to poke around in the source code or borrow/fork it if you want a basic state
machine for your own project.

__GOAL:__
This is a simple repo for showing how to use certain design patterns in Python. The intent is to use software best practices and show an easy to copy demostration of the finite state machine (FSM) pattern using a simulation of a car interacting with a traffic light. 

__DESIGN ISSUE 1: Finite State Machines (Oooo, that's a big scary phrase):__
Finite state machines (FSMs) help programmers get away from the nested conditional logic of stacked if/else blocks and switch statements. Conditionals are an important part of coding, but they often tend to turn into creeping piles of 'spaghetti code'. Creating a big block of conditional logic seems an easy solution when 'in the code', but may end up being burdensome and overcomplicated in hindsight. FSMs deal with this by creating a 'state machine' which delegates responsibility to states for managing when they transition from one to another. 

__Traffic Light FSM:__
There are three typical states for a given traffic light: red light (stop); yellow light (slow down); and green light (go already). This machine ads a fourth state to cover errors, and might be analogous to a blinking red light or a light being off due to a blown transformer. This beautiful ASCII diagram illustrates the states and their transitions.

                _____'change'_____
               |      |    |      |
               |Green |--> |Yellow|
               |______|    |______|
                    ^           |
                    |           | 'change'
                    |       ____V__  
                    |______|       |
               'change'    |  Red  | 
                           |_______|

__Car FSM:__
The car FSM corresponds to a car, and its three states--braking, driving, and coasting--are the three states for a driver responding to the states in a traffic light. In addition, once again, there is a state for handling errors ('Car_ErrorState'). In order to keep this simple, the car accepts the traffic light as an argument and accesses its state attribute directly. There are better ways to do this for big projects, but for now,this repo is to serve as a teaching tool. One FSM-based object (car) with a simple FSM is responding directly to the state changes in another (trafficlight).

By the way, as you can see, doing an ASCII diagram (or a proper UML/State diagram) gets complicated pretty quickly. 

                                        Red--|
          r---> ________             ___|____V
     Red  |    |        |  Green    |        |<-----------------|
          -----|Braking |-------->  |Driving |------Green       |
               |________|----|      |________|<-;     |         |
                    ^        | Yellow  |        |_____|         |
                Red |        V         |                        |
                    |       ___________V                        |
                    |______|            |<--Yellow\             |
                           |  Coasting  |         |             |
                           |____________|<---------             |
                               |                                |
                               |________________________________Green

__SO HOW IS THIS BETTER THAN AN IF/ELSE BLOCK:__
Fair Question, Mr. Person-Who-Didn't-Even-Ask. Ok, so the benefit is that a downstream coder can just take the car state machine and the traffic light state machine and put them together in a program without worrying about how to handle their state logic. They've been programmed to handle that for themselves. It's basically programming two robots that just know how to interact with each other. You see this all the time in video games when NPCs from different factions and classes deal with each other and with the player. The coder writing code for Level 2 doesn't rewrite any of the logic for the bad guys, he drops a bad guy and a good guy where he needs them and lets luck sort it out. Let's see that with the next step (client code) ...

__CLIENT CODE: CROSSWALK__
So the goal here is for a simple simulation of a crosswalk wherein a car comes up and faces a traffic light. When it does, the car will be able to change state in response to the light without the code in Crosswalk having to concern itself with all the state transitions of the two object types. This may not be all that impressive a simulation, but these objects could interact in a more complicated simulation. 