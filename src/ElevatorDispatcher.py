import config
import threading
import time

class ElevatorDispatcher:
  def __init__(self, floors, elevators):
    self.floors = floors
    self.elevators = elevators
    self.floor_counter = 0
    self.elevator_counter = -1

  def run_thread(self):
    self.thread = threading.Thread(target=self.run, daemon=True)
    self.thread.start()

  def run(self):
    while True:
      # look for next floor with at least 1 passenger
      # remember last processed floor so we don't favor bottom floors
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
        # pick an elevator to add the passenger to (Round Robin)
        self.elevator_counter += 1
        picked_elevator = self.elevator_counter % len(self.elevators)
        # find first elevator whose capacity hasn't been reached
        while len(self.elevators[picked_elevator].passengers) >= self.elevators[picked_elevator].capacity:
          picked_elevator += 1
        # TODO: above assumes that there is always an elevator that hasn't reached capacity
        # add the passenger to the picked elevator
        print('passenger with boarding_floor {0} and exit_floor {1} has been assigned to elevator {2}'.format(next_passenger.boarding_request.floor, next_passenger.exit_request.floor, picked_elevator))
        self.elevators[picked_elevator].add_passenger(next_passenger)

      time.sleep(config.SINGLE_TIME_UNIT)