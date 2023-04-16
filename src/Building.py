import random
import math
import threading
import time
import config
from Floor import Floor
from Elevator import Elevator
from ElevatorDispatcher import ElevatorDispatcher
from Request import Request
from Passenger import Passenger


class Building:
  """
  Represents the entire building. 
  
  Holds the list of floors, elevators, and the elevator dispatcher and starts each
  of their respective threads.  Also generates new passengers, and handles 
  drawing the simulation with pygame.

  Attributes:
      floors: List of Floor objects.
      elevators: List of Elevator objects.
      pygame: Pygame controller.
      screen: Screen object used by pygame.
      elevator_dispatcher: ElevatorDispatcher instance.
  """
  
  def __init__(self, num_floors, num_elevators, pygame, screen):
    self.floors = []
    self.create_floors(num_floors)
    self.elevators = []
    self.create_elevators(num_elevators)
    self.pygame = pygame
    self.screen = screen
    self.elevator_dispatcher = ElevatorDispatcher(self.floors, self.elevators)
    self.elevator_dispatcher.run_thread()


  def create_floors(self, num_floors):
    """
    Instantiates Floor objects and adds them to floors list
    """
    for i in range(num_floors):
      self.floors.append(Floor(i))

  def create_elevators(self, num_elevators):
    """
    Instantiates Elevator objects, adds them to elevators list, and starts their threads
    """
    for i in range(num_elevators):
      elevator = Elevator(i)
      self.elevators.append(elevator)
      elevator.runThread()

  def run_thread(self):
    """
    Creates and starts primary thread to generate
    """
    self.thread = threading.Thread(target=self.run, daemon=True)
    self.thread.start()

  def run(self):
    """
    Generates a new passenger every NEW_PASSENGER_TIMEOUT seconds
    """
    while True:
      self.generate_passenger()
      time.sleep(config.NEW_PASSENGER_TIMEOUT)

  def generate_passenger(self):
    '''
    Generates a new passenger request with a random boarding floor, direction
    (up or down button press), and exit floor based on the boarding floor and direction.
    Adds the new Passenger to the boarding floor's Passenger queue.
    '''
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

  def run_graphics_thread(self):
    """
    Creates and starts graphics thread
    """
    self.graphics_thread = threading.Thread(target=self.run_graphics, daemon=True)
    self.graphics_thread.start()

  def run_graphics(self):
    """
    Draws screen every SINGLE_TIME_UNIT seconds
    """
    while True:
      self.draw_screen()
      time.sleep(config.SINGLE_TIME_UNIT)

  def draw_screen(self):
    """
    Contains all of the pygame drawing logic.
    Draws each floor and waiting passengers on that floor and 
    each elevator and passengers assigned to that elevator.
    """
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BORDER_WIDTH = 3
    PADDING = 5
    SCREEN_WIDTH, SCREEN_HEIGHT = self.screen.get_size()
    FLOOR_HEIGHT = SCREEN_HEIGHT / len(self.floors)
    COMPONENT_WIDTH = (SCREEN_WIDTH - (PADDING * (len(self.elevators) + 2))) / (len(self.elevators) + 1)
    COMPONENT_HEIGHT = FLOOR_HEIGHT - (PADDING * 2)
    PASSENGER_RADIUS = 10
    PASSENGER_COLS = COMPONENT_WIDTH / ((PASSENGER_RADIUS * 2) + PADDING)

    self.screen.fill(WHITE)

    for floor in self.floors:
      # draw floor outline
      floor_y = SCREEN_HEIGHT - ((floor.floor_num + 1) * FLOOR_HEIGHT)
      (x, y, width, height) = (0, floor_y, SCREEN_WIDTH, FLOOR_HEIGHT)
      self.pygame.draw.rect(self.screen, BLACK, (x, y, width, height), width=BORDER_WIDTH)

      # draw floor waiting room
      waiting_room_x = x + PADDING
      waiting_room_y = y + PADDING
      self.pygame.draw.rect(self.screen, RED, (waiting_room_x, waiting_room_y, COMPONENT_WIDTH, COMPONENT_HEIGHT))

      # draw floor passengers in waiting room
      if len(floor.passengers) > 0:
        for idx, passenger in enumerate(list(floor.passengers)):
          passenger_x = waiting_room_x + ((idx % PASSENGER_COLS) * (PASSENGER_RADIUS * 2)) + (PASSENGER_RADIUS)
          passenger_y = waiting_room_y + ((math.floor(idx / PASSENGER_COLS)) * (PASSENGER_RADIUS * 2)) + (PASSENGER_RADIUS)
          self.pygame.draw.circle(self.screen, YELLOW, (passenger_x, passenger_y), PASSENGER_RADIUS)

    for elevator in self.elevators:
      # draw elevator
      elevator_x = COMPONENT_WIDTH + (elevator.elevator_num * COMPONENT_WIDTH) + ((elevator.elevator_num + 2) * PADDING)
      elevator_y = SCREEN_HEIGHT - ((elevator.current_floor + 1) * FLOOR_HEIGHT) + PADDING
      self.pygame.draw.rect(self.screen, BLUE, (elevator_x, elevator_y, COMPONENT_WIDTH, COMPONENT_HEIGHT))

      # draw current_passenger
      if elevator.current_passenger is not None:
        current_passenger_x = elevator_x + PASSENGER_RADIUS
        current_passenger_y = elevator_y + PASSENGER_RADIUS
        self.pygame.draw.circle(self.screen, YELLOW, (current_passenger_x, current_passenger_y), PASSENGER_RADIUS)

      # draw elevator passengers in queue
      if len(elevator.passengers) > 0:
        for idx, passenger in enumerate(list(elevator.passengers)):
          passenger_idx = idx if elevator.current_passenger is None else idx + 1
          passenger_x = elevator_x + (passenger_idx % PASSENGER_COLS) * (PASSENGER_RADIUS * 2) + (PASSENGER_RADIUS)
          passenger_y = elevator_y + (math.floor(passenger_idx / PASSENGER_COLS)) * (PASSENGER_RADIUS * 2) + (PASSENGER_RADIUS)
          self.pygame.draw.circle(self.screen, YELLOW, (passenger_x, passenger_y), PASSENGER_RADIUS)

    self.pygame.display.flip()