import argparse
import time
import sys
import os
import pygame
from pygame.locals import *
import config
from Building import Building

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--floors', type=int,
        help="number of floors to simulate, default is {0}".format(config.DEFAULT_NUM_FLOORS), 
        default=config.DEFAULT_NUM_FLOORS)
    parser.add_argument('-e', '--elevators', type=int,
        help="number of floors to simulate, default is {0}".format(config.DEFAULT_NUM_ELEVATORS), 
        default=config.DEFAULT_NUM_ELEVATORS)
    args = parser.parse_args()

    print('Starting simulation with {0} floors and {1} elevators!'.format(args.floors, args.elevators))

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Elevator Simulation')

    building = Building(args.floors, args.elevators, pygame, screen)
    building.run_thread()
    building.run_graphics_thread()

    # listen for user graphics window exit
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.quit()


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print('Interrupted')
    try:
      sys.exit(130)
    except SystemExit:
      os._exit(130)