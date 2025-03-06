
#h = spaces from exit (to red car X) and number of cars in the way (that line)
from collections import deque
import heapq
import sys

"""
Used this website for priority queue information 
HEAPQ - heap queue algorithm. Python documentation. (n.d.). 
https://docs.python.org/3/library/heapq.html 
"""

class Vehicle: 
  #class to define each vehicle given id, coordinate and orientation
  def __init__(self, name, x, y, direction):
    self.id = name #Letter
    self.x = x #0-5
    self.y = y #0-5
    self.direction = direction #V or H
    self.length = 3 if name in 'OPQR' else 2

  def move(self, direction):
        """ Returns a new Vehicle object with updated position 
            given a direction (LRUD) """
        if direction == 'L':
         #   print("in llllllllthis fr")
            return Vehicle(self.id, self.x - 1, self.y, self.direction)
        elif direction == 'R':
          #  print("in this rrrrrrrrrrrrrrrfr")
            return Vehicle(self.id, self.x + 1, self.y, self.direction)
        elif direction == 'U':
          #  print("in this uuuuuuuuuufr")
            return Vehicle(self.id, self.x, self.y - 1, self.direction)
        elif direction == 'D':
          #  print("in this ddddddddfr")
            return Vehicle(self.id, self.x, self.y + 1, self.direction)
      #  print("in this fr")
        return self  # No change

  #priotize cars that are directly touching the red car

def heuristic1(vehicles, board): #how far red car is from exit
        totalBlock = 0
        #spaces from exit 
        for car in vehicles:
          if car.id == 'X':
            redCarx = car.x
        for car in vehicles:
          if car.id != 'X':
            if car.x > redCarx and board[2][car.x] != '.':
              totalBlock += 1

        return totalBlock

def heuristic2(vehicles, board): #blocking cars priortize cars in the way 
        totalBlock = 0
        #spaces from exit and number of cars in the way
        for car in vehicles:
          if car.id == 'X':
            redCarx = car.x
            totalBlock += 4 - redCarx
        for car in vehicles:
          if car.id != 'X':
            if car.x > redCarx and board[2][car.x] != '.':
              totalBlock += 1

        return totalBlock

def getState(vehicles):
    """Returns a hashable representation of the board state."""
    return tuple((v.id, v.x, v.y) for v in vehicles)


def applyMove(vehicles, move):
    """Returns a new list of vehicles after applying a move.
      given a move (which contains a direction (LRUD)and the id
      apply the move to that vehicle and apppend to moves list"""
    direction, vid = move
    new_vehicles = []
    
    for v in vehicles:
        if v.id == vid:
          #  print("wnet in here")
            new_vehicles.append(v.move(direction))
            
        else:
            new_vehicles.append(v)
    
    return new_vehicles



def solveRushHour(vehicles, heuristicIn, max_depth=1):
    """Uses Best-First Search (or A*) to solve Rush Hour.
      also takes in a heuristic value and a max-depth"""

    queue = []  # Priority queue (min-heap)
   # print(vehicles)
    # Push the initial state into the queue: (priority, heuristic, move history, depth, new_vehicles)
    heapq.heappush(queue, (0, 0, [], 0, vehicles))  # (priority, heuristic, move history, depth, new_vehicles)

    visited = set() #track visited states 
    depth_levels = {}  # Track number of nodes at each depth

    while queue:
        # Pop the lowest-cost state from the priority queue
        _, h_value, move_history, depth, current_vehicles = heapq.heappop(queue)

        board = printBoard(current_vehicles)
      #  printIt(board)
      #  print("\n****************")
      #  printIt(board)

        # Track number of nodes at this depth
        if depth not in depth_levels:
            depth_levels[depth] = 0
        depth_levels[depth] += 1

        # Check if red car 'X' is at the exit (5,2) → Puzzle solved!
        for v in current_vehicles:
            if v.id == 'X' and v.x == 4:
                print(f"\nSOLUTION FOUND (with heuristic {heuristicIn}):")
                printIt(board)
                #for d in sorted(depth_levels.keys()):
                #    print(f"Depth {d}: {depth_levels[d]} nodes") #print number of nodes found at each level
                  #print(depth_levels[d])
                  #print(d)
                return move_history  # Return solution path

        # Stop searching if we reached max depth
        if depth >= max_depth:
            continue

        # Get current state and check if it's already visited
        state = getState(current_vehicles)
        if state in visited:
            continue
        visited.add(state)

        # Generate possible moves
        moves = allMoves(current_vehicles, board)

        for move in moves:
            new_vehicles = applyMove(current_vehicles, move)
            
            # Compute heuristic based on the chosen heuristic function
            if heuristicIn == 0:
                heuristic = 0  # Regular BFS (all heuristics are 0)
            elif heuristicIn == 1:
                heuristic = heuristic1(new_vehicles, board)  # Call heuristic1 function
            elif heuristicIn == 2:
                heuristic = heuristic2(new_vehicles, board)  # Call heuristic2 function

            new_priority = heuristic + depth + 1  # f(n) = g(n) + h(n)

            # Push the new state into the priority queue (without Vehicle comparison)
            swapped_move = (move[1], move[0])
            heapq.heappush(queue, (new_priority, heuristic, move_history + [swapped_move], depth + 1, new_vehicles))
    
    #when solution not found still print the summary 
    print("\nNodes per depth level:")
    for d in sorted(depth_levels.keys()):
        print(f"Depth {d}: {depth_levels[d]} nodes")
    
    print("\nMax depth reached, no solution found within given depth limit.")
    return None



def allMoves(vehicles, board):
    """ Returns a list of possible moves based on a baord setup"""
    moves = []
    for vehicle in vehicles: #get coordinates of vehicle
      x = vehicle.x
      y = vehicle.y
      length = vehicle.length
      if vehicle.direction == 'H':
        if x > 0 and board[y][x-1] == '.':
            moves.append(('L', vehicle.id ))
        if x+length < 6 and board[y][x+length] == '.':
            moves.append(('R', vehicle.id))

      if vehicle.direction == 'V':
        if y > 0 and board[y-1][x] == '.':
          moves.append(('U', vehicle.id))
        if y+length < 6 and board[y+length][x] == '.': 
          moves.append(('D', vehicle.id))
    return moves

'''
def goal_state(vehicle):
  for car in vehicle:
    if vehicle.id == 'X':
      if vehicle.x == 4:
        return True
  return False

def bfs_search(start_state, goal_state):
  queue = [[start_state]]
  seen_states = set()
  seen_states.add(start_state)
  while queue:
    path = queue.pop(0)
    if path[-1] == goal_state:
      return True
    for next_state in get_next_states(path[-1]):
      if next_state not in seen_states:
        seen_states.add(next_state)
        queue.append(path + [next_state])
  return False
  '''

def printIt(board): #prints board representation in a nice layout 
  for row in board:
    print(" ".join(row))

def printBoard(vehicle): #returns a list of the vehicles placed on the board
  board = [
    ['.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.'],  # 'X' needs to go to (5,2)
    ['.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.']
  ]
  for car in vehicle:
    name = car.id
    if car.direction == 'V':
      for y in range(car.length):
        board[car.y + y][car.x] = name
    if car.direction == 'H':
      for x in range(car.length):
        board[car.y][car.x + x] = name
  
 # for row in board:
 #   print(" ".join(row))
  return board

'''Create empty list to store all vehicles based on file input '''
vehicle = []
#vehicle.append(Vehicle('A', 0, 0, 'H'))
#vehicle.append(Vehicle('P', 0, 1, 'V'))
#vehicle.append(Vehicle('B', 0, 4, 'V'))
#vehicle.append(Vehicle('X', 1, 2, 'H'))
#vehicle.append(Vehicle('Q', 3, 1, 'V'))
#vehicle.append(Vehicle('R', 3, 5, 'H'))
#vehicle.append(Vehicle('C', 4, 1, 'H'))
#vehicle.append(Vehicle('O', 5, 2, 'V'))
#vehicle.append(Vehicle('F', 0, 4, 'H'))
#vehicle.append(Vehicle('D', 4, 5, 'H'))
#vehicle.append(Vehicle('G', 3, 5, 'H'))
#vehicle.append(Vehicle('E', 3, 3, 'H'))



#open the file
for line in sys.stdin:
  line = line.strip() 
  carId = line[0]
  carx = int(line[1])
  cary = int(line[2])
  carDir = line[3]
  vehicle.append(Vehicle(carId, carx, cary, carDir))
  #print(line.strip())

#file.close()

board = printBoard(vehicle)
printIt(board)

solution = solveRushHour(vehicle, 0, 100)
for item in solution:
  print(f"{item[0]}{item[1]}")
#print(solution)

solution = solveRushHour(vehicle, 1, 100)
for item in solution:
  print(f"{item[0]}{item[1]}")

solution = solveRushHour(vehicle, 2, 100)
for item in solution:
  print(f"{item[0]}{item[1]}")