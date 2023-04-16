# elevator-simulator-python
Blustaq Pre-Interview Code Challenge - The Elevator
---

## Description
This program simulates elevator scheduling in a building of any size with any number of elevators. Each elevator as well as the dispatcher and passenger generator each run on its own thread to simulate elevators running concurrently. The current approach uses a round-robin-like algorithm to assign jobs to elevators, and a First Come First Serve (FCFS) algorithm to process jobs. 


## Usage
    usage: main.py [-h] [-f FLOORS] [-e ELEVATORS]
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FLOORS, --floors FLOORS
                            number of floors to simulate, default is 5
      -e ELEVATORS, --elevators ELEVATORS
                            number of floors to simulate, default is 5


## Assumptions
- It always takes 1 unit of time to move 1 floor
- There are no open/close/start/stop acceleration changes
- Passengers enter and exit the elevator instantaneously
- There is a new passenger request at regular intervals 
- There is no favoring of boarding or exit floors
- Passengers will continue to make new requests even if there are already a lot of people waiting


## Components & Threads
### Building
Represents the entire building. Holds the list of floors, elevators, and the elevator dispatcher and starts each of their respective threads. Also generates new passengers, and handles drawing the simulation with pygame.
- Main thread handles drawing the simulation with pygame.
- Another thread generates new passengers.

### Elevator
Represents a single elevator with a queue of passengers to process and details about its current state. It processes each of its passengers sequentially as they're assigned (big flaw in this means there's only ever one person on any elevator at a time, very inefficient).
- Primary thread processes each passenger that has been assigned to the elevator using a FCFS approach by pulling each passenger from its queue sequentially, moving towards the next passenger's boarding floor, and then moving towards their exit floor.

### Elevator Dispatcher
Determines which elevator to assign passengers to.
- Primary thread looks for the next passenger to be assigned and the next elevator to assign that passenger to, both using a kind of round-robin approach.

### Floor
Data structure representing a floor in the building with a queue of passengers waiting to be assigned to an elevator.

### Passenger
Data structure representing a single passenger with a boarding and exit request.

### Request
Data structure representing either a boarding or exit request of a passenger, with a floor and a direction.


## Next Steps
- More complicated scheduling algorithms:
    - Round Robin
    - Shortest Job First (SJF)
    - Shortest Remaining Time First (SRTF)
    - Elevator (SCAN)
    - Priority Scheduling
    - Load Balancing (dispatching passengers on elevators together who are going to the same floor)
- More complicated population algorithms:
    - Up Peak (more requests at the beginning/middle/end of the day)
    - Zoning (more requests going to particular floors, such as the lobby or a floor with a cafeteria)
- More human-like qualities of passengers
    - Passengers accidentally hitting the wrong buttons
    - Passengers who are uncomfortable sharing an elevator at/near max capacity
    - Passengers who avoid making new requests if there is already a long line of people waiting
- Different architectural designs
    - Double decker elevators
    - Elevators at different sides of the building
- General program improvements
    - Implement changes in velocity for starting/stopping/opening/closing and waiting for passengers to load and unload
    - Output statistics for multiple different inputs (different #'s of floors and elevators)
    - Better GUI (In general, but also specifically, showing passengers still waiting at floor until they're actually picked up by an elevator)
    - Probably better error handling