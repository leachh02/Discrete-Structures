import importlib
import importlib.util
import sys
import traceback
import math

if len(sys.argv) != 3:
   print('''
Error: you must provide a filename for your pegs solution and your student ID

Make sure that this file is located in the same directory as your solution, along with 
probability.py if you use it.  Open a terminal, navigate to the directory containing this file, 
and run

python problem_solving_tester.py problem_solving.py n1234567

replace n1234567 with your student ID.
replace problem_solving.py with the name of your solution file if it is different.
''')
   sys.exit(1)
try:
   filename = sys.argv[1]
   studentid = sys.argv[2]

   spec = importlib.util.spec_from_file_location('problem_solving', filename)
   if spec is None:
      print('''Error when loading the solution file.  There may be syntax errors, the file might not be valid Python code, or the file might not exist.''')
      sys.exit(1)
   problem_solving = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(problem_solving)
except Exception:
   print("Problem parsing the solution:")
   traceback.print_exc()
   sys.exit(1)

numtopics = 0

censortests = [
   ('The cat ate a mouse.', '### cat ate # mouse.'),
   ('I went to the store.', 'I went to ### store.'),
   ('A cookie is a very nice thing', '# cookie is # very nice thing'),
   ('THe thing over there.is.tHe.best!', '### thing over there.is.###.best!'),
   ('aN-otter-ate-An-apple.', '##-otter-ate-##-apple.'),
   ("Don't change anything!", "Don't change anything!")
]
if 'censor' in dir(problem_solving):
   numtopics += 1
   try:
      print('==================================================================================')
      print('Attempting censor topic')
      for text, result in censortests:
         print('----------------------------------------------------------------------------------')
         sol = problem_solving.censor(text)
         if text != result: result = f'{result} <{studentid}>'
         feedback = 'Correct!' if sol == result else 'Incorrect.'
         print(f'Text:           {text}')
         print(f'Result:         {sol}')
         print(f'Desired result: {result}')
         print(feedback)
   except Exception:
      print('Problem running censor function')
      traceback.print_exc()

fertilisertests = [
   ((1.0, 0.0, 0.0, 1.0, 2.0, 2.0), (2.0,  2.0)),
   ((0.3, 0.2, 0.1, 0.4, 10,  20 ), (20.0, 40.0)),
   ((0.111, 0.444, 0.322, 0.211, 5.7545, 10.111 ), (17.07732105364418, 11.984215413184772)),
   ((0.5, 0.5, 0.5, 0.3, 10,  2  ), None),
   ((0.3, 0.3, 0.3, 0.3, 10,  20 ), None)
]

if 'fertiliser' in dir(problem_solving):
   numtopics += 1
   try:
      print('==================================================================================')
      print('Attempting fertiliser topic')
      for args, result in fertilisertests:
         print('----------------------------------------------------------------------------------')
         an, ap, bn, bp, n, p = args
         print(f'Function arguments: an = {an} ap = {ap} bn = {bn} bp = {bp} n = {n} p = {p} ')
         sol = problem_solving.fertiliser(*args)
         
         if sol is None:
            print(f'Result:         None')
            print(f'Desired result: {str(result)}')
            if sol == result:
               print('Correct!')
            else:
               print('Incorrect.')
         elif type(sol) is tuple:
            if result is None:
               print(f'Result:         {sol}')
               print(f'Desired result: {str(result)}')
               print('Incorrect.')
               continue
            if len(sol) != 2:
               print(f'Expected a tuple of length two, got {sol}')
            else:
               a, b = sol
               aresult, bresult = result
               print(f'Result:         a = {a} b = {b}')
               print(f'Desired result: a = {aresult} b = {bresult}')
               if abs(a - aresult) > 0.001 or abs(b - bresult) > 0.001:
                  print('Incorrect.')
               else:
                  print('Correct!')
         else:
            print(f'Expected None or a tuple of length 2.  Got {str(sol)}')

   except Exception:
      print('Problem running fertiliser function')
      traceback.print_exc()


if 'makeBet' in dir(problem_solving):
   numtopics += 1
   try:
      print('==================================================================================')
      print('Attempting makeBet topic')
      print('----------------------------------------------------------------------------------')
      import random
      random.seed(0)
      totalprofit = 0.0
      numberOfRounds = 10000
      for round in range(numberOfRounds):
         if random.randint(0,1) == 0:
            headsprob = 0.7
         else:
            headsprob = 0.4

         previousOutcome = None
         state = None
         profit = 0.0
         odds = dict()
         for _ in range(100):
            odds['heads'] = random.uniform(1, 3)
            odds['tails'] = random.uniform(1, 3)
            
            bet, state = problem_solving.makeBet(odds['heads'], odds['tails'], previousOutcome, state)
            
            previousOutcome = 'heads' if random.random() < headsprob else 'tails'
            if bet == previousOutcome:
               profit += odds[bet] - 1
            elif bet != 'no bet':
               profit -= 1          # stake lost


         #print("Probability of heads was", headsprob, "Profit was", profit)
         totalprofit += profit
      averageprofit = totalprofit / numberOfRounds
      print("Average profit per run:", averageprofit)
      marks = math.ceil(7 * averageprofit / 33.5)
      print(f"Estimated number of marks: {marks}")

   except Exception:
      print('Problem running makeBet function')
      traceback.print_exc()

print()
print('''If the your solution is correct for the first test case, but not for subsequent
cases then you may have variables that are only initialised once, and not for each time 
each your function is run.  This is likely to be a problem if you use global variables.
   ''')

if numtopics < 2:
   print("Warning!  Fewer than two topics attepmted!")