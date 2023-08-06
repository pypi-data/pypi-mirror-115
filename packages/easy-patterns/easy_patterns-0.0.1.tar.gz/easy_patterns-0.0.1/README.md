# easy_patterns
Demonstrator for teaching design patterns in Python

__GOAL:__
This is a simple repo for showing how to use certain design patterns in Python. The intent is to use software best practices and show an easy to copy demostration of the finiste state machine (FSM) pattern using a simulation of a car interacting with a traffic light. 

__DESIGN ISSUE 1: Finite State Machines (Oooo, that's a big scary phrase):__
Finite state machines (FSMs) help programmers get away from the nested conditional logic of stacked if/else blocks and switch statements, which tend to turn into creeping piles of 'spaghetti code'. The logic always seems easy when 'in the code', but often becomes burdensome and overcomplicated in hindsight (ie: when trying to change or fix something some time after writing it). FSMs deal with this by giving each 'state' responsibility for the logic of when and how to change state, and delegating the state-change to a machine encapsulating the states. As a simple example, if there is a videogame with an NPC, the NPC's aggression (aggro) will likely be managed by dropping an FSM into it. The FSM may change based on alliances/etc, but the FSM will manage the states (AttackingState, RetreatingState, NeutralState, etc).

__Traffic Light FSM:__
There are three states for a given traffic light: red light (stop); yellow light (slow down); and green light (go already). This beautiful ASCII diagram illustrates the states and their transitions.

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
The car FSM corresponds to a car, and its three states--braking, driving, and coasting--are the three states for a driver responding to the states in a traffic light. In order to keep this simple, the car accepts the traffic light as an argument and accesses its state attribute directly. There are better ways to do this for big projects, but for now,this repo is to serve as a teaching tool. One FSM-based object (car) with a simple FSM is responding directly to the state changes in another (trafficlight).

By the way, as you can see, doing an ASCII diagram (or a proper UML/State diagram) gets complicated pretty quickly. 

                                        Red--|
          ----> ________             ___|____V
     Red  |    |        |  Green    |        |<-----------------|
          -----|Braking |-------->  |Driving |------Green       |
               |________|----|      |________|<_      |         |
                    ^        | Yellow  |        |_____|         |
                Red |        V         |                        |
                    |       ___________V-Yellow---|             |
                    |______|            |         |             |
                           |  Coasting  |         |             |
                           |____________|<---------             |
                               |                                |
                               |________________________________Green

__SO HOW IS THIS BETTER THAN AN IF/ELSE BLOCK:__
Fair Question, person who didn't even ask it. Ok, so the benefit is that a downstream coder can just take the car and the traffic light, and put them together in a program without worrying about the state logic. It's like having a couple of robots and putting them somewhere. Drop and go. You see this in video games when NPCs interact with each other, or when they interact with the player. The coder writing code for Level 2 doesn't rewrite any of the logic for the bad guys, he just clones a bad guy and drops it in place. Let's see that with the next step (client code) ...

__CLIENT CODE: CROSSWALK__
So the goal here is for a simple simulation of an intersection wherein a car comes up and faces a traffic light. When it does, the car will be able to change state in response to the light without the code in Crosswalk having to concern itself with all the state transitions of the two object types.