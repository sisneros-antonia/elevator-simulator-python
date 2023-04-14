import config
from collections import deque
import threading
import time

class Elevator:
  def __init__(self, elevator_num):
    self.elevator_num = elevator_num
    self.capacity = config.ELEVATOR_CAPACITY
    self.current_floor = 0
    self.passengers = deque()
    self.current_passenger = None

  def add_passenger(self, passenger):
    self.passengers.append(passenger)

  def runThread(self):
    self.thread = threading.Thread(target=self.run, daemon=True)
    self.thread.start()

  def run(self):
    while True:
      if self.current_passenger:
        self.process_current_passenger()
      elif len(self.passengers) != 0:
        # get next passenger from queue
        self.current_passenger = self.passengers.popleft()
        self.process_current_passenger()

      time.sleep(config.SINGLE_TIME_UNIT)

  def process_current_passenger(self): # (FCFS)
    if self.current_passenger.boarding_request:
      boarding_floor = self.current_passenger.boarding_request.floor
      floor_increment = -1 if boarding_floor < self.current_floor else 1
      self.current_floor += floor_increment
      # remove current_passenger's boarding_request if elevator made it to the boarding floor
      if self.current_floor == boarding_floor:
        print('Passenger boarding: Elevator {0} has made it to a boarding floor {1}'.format(self.elevator_num, boarding_floor))
        self.current_passenger.boarding_request = None
    else:
      exit_floor = self.current_passenger.exit_request.floor
      floor_increment = 1 if exit_floor > self.current_floor else -1
      self.current_floor += floor_increment
      # remove current_passenger if elevator made it to the exit floor
      if self.current_floor == exit_floor:
        print('Passenger exiting: Elevator {0} has made it to a exit floor {1}'.format(self.elevator_num, exit_floor))
        self.current_passenger = None