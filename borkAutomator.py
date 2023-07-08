import random
class Bork:
   exitsMap = {
      'Home': { 'Future': 'Heat death of the universe', 'East': 'Swamp', 'West': 'Town' },
      'Town': { 'South': 'Home', 'North': 'Forest' },
      'Swamp': { 'West': 'Town', 'Hubward': 'Sagitarius A*' },
      'Forest': { 'East': 'Swamp', 'widdershins': 'Heat death of the universe' },
      'Big bang': { 'Futast': 'Forest',  'turnwise': 'Home'},
      'Sagitarius A*': { 'Pasorth': 'Big bang', 'rimwards': 'Town' },
      'Heat death of the universe': { 'Past': 'Sagitarius A*' }
   }
   startLocation = 'Home'

   def __init__(self, hardCore = False):
      self.hardCore = hardCore
      self.location = self.startLocation
      self.saveGames = dict()
   
   def restart(self):
      self.location = self.startLocation

   def description(self):
      return self.location

   def exits(self):
      return set(self.exitsMap[self.location].keys())

   def move(self, exit):
      if exit not in self.exits():
         raise ValueError(f"Attempted to move to non-existant exit {exit} from location {self.location}.")
      self.location = self.exitsMap[self.location][exit]

   def save(self):
      if self.hardCore:
         raise ValueError('Attempted to save in hard-core mode!')
      saveGame = random.randint(0, 2**29)
      self.saveGames[saveGame] = self.location
      return saveGame
   
   def restore(self, saveGame):
      if self.hardCore:
         raise ValueError('Attempted to restore in hard-core mode!')
      if saveGame not in self.saveGames:
         raise ValueError("Attempted to restore a non-existant save game.")
      
      self.location = self.saveGames[saveGame]      
