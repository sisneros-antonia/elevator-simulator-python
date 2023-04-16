import config
from collections import deque
import threading
import time

class Elevator:
  """
  Represents a single elevator with a queue of passengers to process and details
  about its current state. 
  
  Its primary thread processes each passenger that has been assigned to the 
  elevator using a FCFS approach by pulling each passenger from its queue 
  sequentially, moving towards the next passenger's boarding floor, and then 
  moving towards their exit floor.

  Attributes:
      elevator_num: Id of the elevator.
      capacity: Max number of passengers that can fit in the elevator.
      current_floor: Elevator's current floor at a specific moment in time.
      passengers: Queue of passenger's that have been assigned to the elevator.
      current_passenger: Passenger that is currently being processed.
  """

  def __init__(self, elevator_num):
    self.elevator_num = elevator_num
    self.capacity = config.ELEVATOR_CAPACITY
    self.current_floor = 0
    self.passengers = deque()
    self.current_passenger = None

  def add_passenger(self, passenger):
    """
    Adds a passenger to the elevator's queue.
    """
    self.passengers.append(passenger)

  def runThread(self):
    """
    Creates and starts the elevator's main processing thread.
    """
    self.thread = threading.Thread(target=self.run, daemon=True)
    self.thread.start()

  def run(self):
    """
    Either continues processing current passenger or gets a new passenger and starts
    processing them, every SINGLE_TIME_UNIT seconds.
    """
    while True:
      if self.current_passenger:
        self.process_current_passenger()
      elif len(self.passengers) != 0:
        # get next passenger from queue
        self.current_passenger = self.passengers.popleft()
        self.process_current_passenger()

      time.sleep(config.SINGLE_TIME_UNIT)

  def process_current_passenger(self): # (FCFS)
    """
    Simple logic to process the current passenger using a FCFS algorithm which always
    moves towards the current passenger's boarding floor if it hasn't yet been reached
    or towards the currrent passenger's exit foor if the boarding floor was previously 
    reached.
    """
    if self.current_passenger.boarding_request:
      boarding_floor = self.current_passenger.boarding_request.floor
      floor_increment = -1 if boarding_floor < self.current_floor else 1
      self.current_floor += floor_increment
      # remove current_passenger's boarding_request if elevator made it to the boarding floor
      if self.current_floor == boarding_floor:
        print('Passenger boarding: Elevator {0} has made it to a boarding floor {1}'
              .format(self.elevator_num, boarding_floor))
        self.current_passenger.boarding_request = None
    else:
      exit_floor = self.current_passenger.exit_request.floor
      floor_increment = 1 if exit_floor > self.current_floor else -1
      self.current_floor += floor_increment
      # remove current_passenger if elevator made it to the exit floor
      if self.current_floor == exit_floor:
        print('Passenger exiting: Elevator {0} has made it to a exit floor {1}'
              .format(self.elevator_num, exit_floor))
        self.current_passenger = None