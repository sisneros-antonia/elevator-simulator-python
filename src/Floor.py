from collections import deque

class Floor:
  def __init__(self, floor_num):
    self.floor_num = floor_num
    self.passengers = deque()