import importlib
import importlib.util
import sys
import traceback
import borkAutomator
import pprint

if len(sys.argv) != 2:
   print('''
Error: you must provide a filename for your bork solution.

Make sure that this file is located in the same directory as your solution, along with 
graphs.py and digraphs.py if you use them.  Open a terminal, navigate to the directory
containing this file, and run

python borktester.py bork.py

replace bork.py with the name of your solution file if it is different.
''')
   sys.exit(1)
try:
   filename = sys.argv[1]
   spec = importlib.util.spec_from_file_location('borksolution', filename)
   if spec is None:
      print('''Error when loading the solution file.  There may be syntax errors, the file might not be valid Python code, or the file might not exist.''')
      sys.exit(1)
   borksolution = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(borksolution)
except Exception:
   print("Problem parsing the solution:")
   traceback.print_exc()
   sys.exit(1)

def checkSolution(solution, realsolution):
   if realsolution != solution:
      print("Solution differs from real map!")
      print("Real map:")
      pprint.pprint(realsolution)
      print("\n\nSolution map:")
      pprint.pprint(solution)
      
      print("\n\nDifferences:")
      if not isinstance(solution, dict):
         print("Solution map is not a dictionary.  Incorrect return format.")
         return False

      for loc in realsolution:
         if loc not in solution:
            print(f"Solution is missing location {loc}")
      
      for loc in solution:
         if loc not in realsolution:
            print(f"Solution has extra location {loc}")

      for loc in solution.keys() & realsolution.keys():
         if solution[loc] != realsolution[loc]:
            print(f"Location {loc} has different exits:")
            print(f'Solution map for {loc}')
            pprint.pprint(solution[loc])
            print(f'Real map for {loc}')
            pprint.pprint(realsolution[loc])
      
      return False

   print("Correct output!")
   return True

maps = [
   ({'A': {'0': 'B', 'AF57352': 'F', 'AH37029': 'H', 'AI3850': 'I', 'AJ62505': 'J'},
   'B': {'1': 'C'},
   'C': {'2': 'D', 'CI64084': 'I'},
   'D': {'3': 'E', 'DF22855': 'F', 'DH32855': 'H'},
   'E': {'4': 'F', 'EG5134': 'G'},
   'F': {'5': 'G', 'FH39272': 'H'},
   'G': {'6': 'H', 'GA38041': 'A', 'GF63731': 'F'},
   'H': {'7': 'I', 'HJ28219': 'J'},
   'I': {'8': 'J', 'IG42493': 'G', 'IH37246': 'H'},
   'J': {'9': 'A', 'JF61209': 'F'}}, 
   'A'),

   ({'A': {'0': 'B', 'AE46085': 'E'},
   'B': {'1': 'C', 'BA48053': 'A'},
   'C': {'2': 'D', 'CA13318': 'A'},
   'D': {'3': 'E', 'DC42356': 'C'},
   'E': {'4': 'A', 'ED8714': 'D'}}, 
   'A'),

   ({'A': {'0': 'B'}, 'B': {'1': 'A'}},
   'A')
]


if 'traverseBork' in dir(borksolution):
   for map, start in maps:
      bork = borkAutomator.Bork()
      bork.exitsMap = map
      bork.startLocation = start
      bork.restart()
      solution = borksolution.traverseBork(bork)
      correct = checkSolution(solution, map)
   
   print('''If the your solution is correct for the first map, but not for subsequent
maps then you may have variables that are only initialised once, and not for each time 
each your function is run.  This is likely to be a problem if you use global variables.
   ''')
else:
   print("Couldn't find traverseBork() function!  Are you sure you provided the correct filename?")

if 'traverseBorkHardCore' in dir(borksolution):
   print("Found hard core mode solver.")
   
   for map, start in maps:
      bork = borkAutomator.Bork(hardCore=True)
      bork.exitsMap = map
      bork.startLocation = start
      bork.restart()
      solution = borksolution.traverseBorkHardCore(bork)
      correct = checkSolution(solution, map)
   
   print('''If the your solution is correct for the first map, but not for subsequent
maps then you may have variables that are only initialised once, and not for each time 
each your function is run.  This is likely to be a problem if you use global variables.
   ''')
else:
   print("Didn't find traverseBorkHardCore() function.")





