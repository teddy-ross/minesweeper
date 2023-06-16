'''
Names: Michael Mercer and Edward Ross
file: minesweeper.py
This is the game engine for minesweeper.
'''


from random import sample


class Minesweeper(object):
   def __init__(self, size, mines):
      self.size = size
      self.board = [[Tile() for col in range(self.size)] for row in range(self.size)]
      self.mines = mines
      self.gameExploded = False
      self.tilesLeft = self.size * self.size - self.mines
      self.flaggedTiles = 0
      self.firstStep = False 
   
   def minesRemaining(self):
      
      return (self.mines - self.flaggedTiles)

   def isExploded(self):
      if self.gameExploded == True:
         
         return True
      else:
         return False

   def getTotalFlags(self):
      return self.flaggedTiles
      
   def isGameOver(self):
      if self.gameExploded or self.tilesLeft == 0:
         return True
      else:
         return False

   def step(self, row, column):
      pressed = self.board[row][column]
      self.tilesLeft -= 1
      if self.firstStep == False: 
         self.placeMine(row, column)
         self.firstStep = True

      if pressed.reveal()==True:
         self.gameExploded = True
     
      else:
         self.spread(row, column)
      
   def spread(self, row, column):

      neighbor = self.board[row][column]
      
      
      if neighbor.neighborMines == 0:
                  
         for x in range(max(0,row-1), min(self.size, row + 2)):
            for y in range(max(0,column - 1), min(self.size, column + 2)):
               #something here that updates neighbor as a tile
               neighbor= self.board[x][y]
               if neighbor.known == False:
                  self.step(x,y)
      
   def flag(self, row, column):
      
      place=self.board[row][column]
      place.toggleFlag()
      if place.flagged==True:
         self.flaggedTiles += 1
      else:
         self.flaggedTiles -= 1
         

      
   def placeMine(self, row, column):
      coords=[]
      for x in range(self.size):
         for y in range(self.size):
            if x != row or y != column: 
               coords.append((x,y))

      if (row, column) in coords:
         coords.remove(row,column)
      bombsSpot= sample(coords, self.mines)
      
      for i in bombsSpot:
         bombRow = i[0]
         bombColumn = i[1]
         if row == bombRow and bombColumn == column:
            print("w")
         bomb = self.board[bombRow][bombColumn]
         bomb.present=True

      #double for loop
      
         for x in range(max(0,bombRow-1), min(self.size, bombRow + 2)):
            for y in range(max(0,bombColumn - 1), min(self.size, bombColumn + 2)):
               
               if x == bombRow and y == bombColumn:
                  continue 
               else: 
                  notBomb = self.board[x][y]
                  notBomb.increaseNeighbors()

   def showAll(self):
      for x in range(self.size):
         for y in range(self.size):
            a=self.board[x][y]
            a.known = True
   
   def getAt(self, row, column):
      boardStringTile = self.board[row][column]
      return str(boardStringTile)


   def isKnown(self, row, column):
      
      knownTile = self.board[row][column]
      return knownTile.known

   def __len__(self):
      return self.size


class Tile(object):

   def __init__(self):

      self.present = False
      self.known = False
      self.exploded = False
      self.flagged = False
      
      self.neighborMines = 0

   def __str__(self):

      if self.flagged == True and self.known != True:
         return "!"
      elif self.known == False:
         return "?"
      elif self.exploded == True:
         return "X"
      elif self.present == True:
         return "*"
      elif self.neighborMines > 0:
         return f'{self.neighborMines}'
      elif self.neighborMines == 0:
          return " " 

   def reveal(self):

      self.known = True

      if self.present == True:
         self.exploded = True
         return True
      else:
         return False

   def increaseNeighbors(self):
      self.neighborMines += 1
      return self.neighborMines
   
   def toggleFlag(self):

      if self.flagged == True:
         self.flagged = False
      else:
         self.flagged = True
      


      
      
      
