import digraphs

# modified from CAB203 graphs.py

# Helper Functions

def allowed_exits(bork, map, location):
   #for first case
   if len(map) == 0:
      return bork.exits()
   #loop of all keys in the map so far and checks if current location is a revisit
   avail_exits = bork.exits()
   for dont_repeat in set(map[location].keys()):
      avail_exits.remove(dont_repeat)
   return avail_exits

def travel_path(start, end, map):
   # vertices found so far
   V = set(map.keys())
   # edges found so far
   E = { (u, Nu[v]) for u, Nu in map.items() for v in Nu }
   # With the current information gathered, find a path from home to desired end point
   path = digraphs.findPath(V, E, start, end)
   #initilaise an array to store list of directions
   path_direction = []
   #there will always be the number of vertices in a path - 1 directions to be taken
   for i in range(len(path) - 1):
      #loops throuhg all directions from a certain vertex in the path
      for direction in set(map[path[i]].keys()):
         #if this direction takes them to the next vertex add the direction to the list
         if map[path[i]][direction] == path[i+1]:
            path_direction.append(direction)
   return path_direction

def travel(bork, given_path):
   #start at initial location
   bork.restart()
   #move however many times neccessary to get to location
   for move in given_path:
      bork.move(move)

def next_to_explore(map):
   #fresh set
   tobechosen = set()
   #check what hasn't been explored
   for locations in set(map.keys()):
      if map[locations] == {}:
         tobechosen.add(locations)
   return tobechosen

def explore(bork, start, end, map):
   # use travel function to get to where you want to be 
   travel(bork, travel_path(start, end, map))
   #the number of exits determines how many times to loop
   times_to_repeat = len(bork.exits())
   for i in range(times_to_repeat):
      travel(bork, travel_path(start, end, map))
      location = bork.description()
      #select an arbitrary exit from a path not travelled
      exit = digraphs.arbitraryElement(allowed_exits(bork, map, location))
      bork.move(exit)
      destination = bork.description()
      map[location].update({ exit: destination })
      #if this place hasnt been visited add it to the map
      if destination not in set(map.keys()):
         map[destination] = {}

def exploreR(bork, init_location, map):
   if next_to_explore(map) == set():
      return
   else:
      explore(bork, init_location, digraphs.arbitraryElement(next_to_explore(map)), map)
      exploreR(bork, init_location, map)


def traverseBork(bork):
   # start and find currrent location (Home)
   map = {}
   bork.restart()
   init_location = bork.description()
   map[init_location] = {}

   exploreR(bork, init_location, map)
   
   return map

# To play in hard core mode, define the function traverseBorkHardCore(bork)
# You shoud also define traverseBork either way!
def traverseBorkHardCore(bork):
   # start and find currrent location (Home)
   map = {}
   bork.restart()
   init_location = bork.description()
   map[init_location] = {}

   exploreR(bork, init_location, map)
   
   return map

# The following will be run if you execute the file like python3 bork_n1234567.py
# Your solution should not depend on this code.
if __name__ == "__main__":
   import borkAutomator
   bork = borkAutomator.Bork()
   print(traverseBork(bork))

   try:
      borkHC = borkAutomator.Bork(hardCore=True)
      print(traverseBorkHardCore(borkHC))
   except NameError:
      print("Not attempting hard core mode")
