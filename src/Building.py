from Floor import Floor
from Elevator import Elevator
from ElevatorDispatcher import ElevatorDispatcher
from Request import Request
from Passenger import Passenger
import random

class Building:
  def __init__(self, num_floors, num_elevators):
    self.floors = []
    self.create_floors(num_floors)
    self.elevators = []
    self.create_elevators(num_elevators)
    self.elevator_dispatcher = ElevatorDispatcher(self.floors, self.elevators)
    self.elevator_dispatcher.run_thread()

  def get_num_floors(self):
    return self.num_floors

  def create_floors(self, num_floors):
    for i in range(num_floors):
      self.floors.append(Floor(i))

  def create_elevators(self, num_elevators):
    for i in range(num_elevators):
      elevator = Elevator(i)
      self.elevators.append(elevator)

      # start elevator's processing thread
      elevator.runThread()

  '''
  Generates a new passenger request with a random boarding floor, direction
  (up or down button press), and exit floor based on the boarding floor and direction.
  Adds a new Passenger to the boarding floor's Passenger queue.
  '''
  def generate_passenger(self):
    boarding_floor = random.randint(0, len(self.floors) - 1)

    ### create boarding request ###
    # if top floor, passenger always hits down button
    # if bottom floor, passenger always hits up button
    # else, choose random direction
    direction = 0
    if boarding_floor == len(self.floors) - 1:
      direction = 0
    elif boarding_floor == 0:
      direction = 1
    else:
      direction = random.choice([0, 1])
    boarding_request = Request(boarding_floor, direction)

    ### create exit request ###
    # choose exit floor based on passenger's boarding floor and requested direction
    exit_floor = 0
    if (direction == 0):
      exit_floor = random.randint(0, boarding_floor - 1)
    else:
      exit_floor = random.randint(boarding_floor + 1, len(self.floors) - 1)
    exit_request = Request(exit_floor, direction)

    # create new passenger and add to floor's passenger queue
    print('Passenger generated with boarding_floor {0} and exit_floor {1}'.format(boarding_floor, exit_floor))
    new_passenger = Passenger(boarding_request, exit_request)
    self.floors[boarding_floor].passengers.append(new_passenger)
  