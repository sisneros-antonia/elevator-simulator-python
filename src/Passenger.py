class Passenger:
  """
  Represents a single passenger with a boarding and exit request. 

  Attributes:
      boarding_request: Request object holding the passenger's boarding details.
      exit_request: Request object holding the passenger's exit details.
  """

  def __init__(self, boarding_request, exit_request):
    self.boarding_request = boarding_request
    self.exit_request = exit_request