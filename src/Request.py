class Request:
  """
  Represents either a boarding or exit request of a passenger.

  Attributes:
      floor: Floor of the request (entering floor if boarding, exiting floor if exit).
      direction: Direction that the passenger requested to move in (up/down button).
  """

  def __init__(self, floor, direction):
    self.floor = floor
    self.direction = direction