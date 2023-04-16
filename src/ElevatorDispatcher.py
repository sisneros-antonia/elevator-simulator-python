import config
import threading
import time

class ElevatorDispatcher:
  """
  Determines which elevator to assign passengers to.

  Attributes:
    floors: List of Floor objects.
    elevators: List of elevator objects.
    floor_counter: Keeps track of which floor to assign a passenger from next.
    elevator_counter: Keeps track of which elevator to assign a passenger to next.
  """

  def __init__(self, floors, elevators):
    self.floors = floors
    self.elevators = elevators
    self.floor_counter = 0
    self.elevator_counter = -1

  def run_thread(self):
    """
    Creates and runs dispatcher's primary thread
    """
    self.thread = threading.Thread(target=self.run, daemon=True)
    self.thread.start()

  def run(self):
    """
    Looks for the next passenger to be assigned and the next elevator to assign 
    that passenger to, both using a kind of round-robin approach.
    """
    while True:
      # look for next floor with at least 1 passenger
      # remember last processed floor so that bottom floors aren't favored
      next_passenger = None
      for i in range(self.floor_counter, len(self.floors)):
        if len(self.floors[i].passengers) > 0:
          self.floor_counter = i
          next_passenger = self.floors[i].passengers.popleft()
          break

      if next_passenger is None:
        for i in range(0, self.floor_counter):
          if len(self.floors[i].passengers) > 0:
            self.floor_counter = i
            next_passenger = self.floors[i].passengers.popleft()
            break
      
      if next_passenger is not None:
        # pick an elevator to add the passenger to
        self.elevator_counter += 1
        picked_elevator = self.elevator_counter % len(self.elevators)
        # find first elevator whose capacity hasn't been reached
        while len(self.elevators[picked_elevator].passengers) >= self.elevators[picked_elevator].capacity:
          picked_elevator += 1
        # add the passenger to the picked elevator
        print('passenger with boarding_floor {0} and exit_floor {1} has been assigned to elevator {2}'
              .format(next_passenger.boarding_request.floor, next_passenger.exit_request.floor, picked_elevator))
        self.elevators[picked_elevator].add_passenger(next_passenger)

      time.sleep(config.SINGLE_TIME_UNIT)