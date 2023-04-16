from collections import deque

class Floor:
  """
  Represents a single floor in the building that holds a queue of passengers
  waiting for an elevator.

  Attributes:
      floor_num: Id of the floor.
      passengers: Queue of Passenger objects waiting to be assigned to an elevator.
  """

  def __init__(self, floor_num):
    self.floor_num = floor_num
    self.passengers = deque()