from Building import Building
import config
import time

def main():
    print('hello world')
    # parse args
    # TODO: for now using hard coded vals
    NUM_FLOORS = 5
    NUM_ELEVATORS = 2
    building = Building(NUM_FLOORS, NUM_ELEVATORS)

    # generate a new passenger every NEW_PASSENGER_TIMEOUT ms
    while True:
      building.generate_passenger()
      time.sleep(config.NEW_PASSENGER_TIMEOUT)


if __name__ == "__main__":
    main()