from Building import Building
import config
import argparse
import time

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
    building = Building(args.floors, args.elevators)

    # generate a new passenger every NEW_PASSENGER_TIMEOUT ms
    while True:
      building.generate_passenger()
      time.sleep(config.NEW_PASSENGER_TIMEOUT)


if __name__ == "__main__":
    main()