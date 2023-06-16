"""
Author: Liz Matthews
File: minesweeperGUI.py

Displays a window with multiple buttons and plays the connect four game.
"""

from breezypythongui import EasyFrame
from tkinter import PhotoImage
from minesweeper import Minesweeper
from os.path import join, exists
import time
import threading
import pickle

class MinesweeperGUI(EasyFrame):

   def __init__(self):
      """Creates the minesweeper game with buttons."""
      super().__init__(title = "Minesweeper", resizable=False)
      
      # Images dictionary to have one PhotoImage per file
      self.images = {
         "!" : PhotoImage(file = join("images","flag.png")),
         "*" : PhotoImage(file = join("images","bomb.png")),
         " " : PhotoImage(file = join("images","empty.png")),
         "?" : PhotoImage(file = join("images","unknown.png")),
         "X" : PhotoImage(file = join("images","explode.png")),
         "." : PhotoImage(file = join("images","smile.png")),
         "S" : PhotoImage(file = join("images","scared.png")),
         "W" : PhotoImage(file = join("images","win.png")),
         "L" : PhotoImage(file = join("images","dead.png"))
      }
      
      for i in range(1, 9):
         self.images[str(i)] = PhotoImage(file = join("images",
                                                      f"{i}.png"))
      
      # Size is 10 x 10
      self.size = 10
      
      # Starts with 10 mines
      self.mines = 10
      
      self.timer = 0
      self.timerGo = False
      
      
      # Create a minesweeper game and set the size appropriately
      self.game = Minesweeper(size=self.size, mines=self.mines)
      
      # Emote to react to your clicks
      self.emote = self.addLabel("", row=0, column=len(self.game)//2)
      self.emote["image"] = self.images["."]
      
      # Label to show how many mines are in the board
      self.minesLabel = self.addLabel(f"Mines: {self.mines}",
                                      row=0, column=0,
                                      columnspan=3)
      
      self.timerLabel = self.addLabel(f"Time: {self.formatTime()}",
                                      row=0, column=len(self.game)//2-2,
                                      columnspan=2)
      
      # Label to show how many unflagged mines are left.
      self.totalMinesLabel = self.addLabel(f"Unflagged Mines: {self.mines-self.game.getTotalFlags()}",
                                      row=0, column=len(self.game)-3,
                                      columnspan=3)
      
      # Create size x size buttons for the game
      self.boardButtons = []
      for row in range(len(self.game)):
         self.boardButtons.append([])
         for column in range(len(self.game)):         
            self.boardButtons[-1].append(self.addButton(row = row+1,
                                                     column = column,
                                                     text = "",
                                                     command=lambda r=row, c=column: self.nextMove(r, c),
                                                     bg="white",
                                                     fg="black",
                                                     rightClick=lambda r=row, c=column: self.flag(r, c),
                                                     pressClick=self.pressClick,
                                                     releaseClick=self.releaseClick))
      # Update the view   
      self.setButtons()
      
      # Add a new game button
      self.newGameButton = self.addButton(row = len(self.game)+1,
                                          column = len(self.game)-2,
                                          columnspan= 2,
                                          text = "New Game",
                                          command = self.newGame,
                                          state = "disabled")
      
      # Add a button for changing the total number of mines
      self.changeMinesButton = self.addButton(row = len(self.game)+1,
                                              column = 0,
                                              columnspan=4,
                                              text = "Change Number of Mines",
                                              command = self.changeMines,
                                              state = "normal")
      
   
   def timerFunc(self):
      while self.timerGo:
         self.timer += 1
         self.timerLabel["text"] = f"Time: {self.formatTime()}"
         time.sleep(1)
   
   def formatTime(self):
      sec     = self.timer % 60
      minutes = self.timer // 60
      return f"{minutes}:{sec:02}"

   
   # For the emoticon at the top
   def pressClick(self):
      self.emote["image"] = self.images["S"]
      
      if not self.timerGo:
         self.timerGo = True
         self.timerThread = threading.Thread(target=self.timerFunc)
         self.timerThread.start()
         
   def releaseClick(self):
      self.emote["image"] = self.images["."]
   
   def changeMines(self):
      """For changing the total number of mines.
      Will call newGame() to reset the board."""
      numMines = self.prompterBox(title = "Number of Mines",
                                 promptString = "How many mines?",
                                 inputText = f"{self.mines}",
                                 fieldWidth = 20)
      if numMines.isnumeric():
         self.mines = max(1,min(self.size**2 - 1,int(numMines)))
         self.minesLabel["text"] = f"Mines: {self.mines}"
         self.newGame()
         
   def setButtons(self):
      """Sets the buttons' text based on the state of the game."""
      for row in range(len(self.game)):
         for col in range(len(self.game)):
            img = self.images[str(self.game.getAt(row, col))]
            self.boardButtons[row][col]["image"] = img
            if self.game.isKnown(row, col):
               self.boardButtons[row][col]["state"] = "disabled"
               
      self.totalMinesLabel["text"] = f"Unflagged Mines: {self.game.minesRemaining()}"
      
   def flag(self, row, column):
      """Called when right-click is pressed on a button."""
      self.game.flag(row, column)
      self.setButtons()

   def nextMove(self, row, column):
      """Makes a move in the game and updates the view with
      the results."""
     
      # Update the model and view
      self.game.step(row, column)
      self.setButtons()
      
      # Detect game over
      if self.game.isGameOver():
         self.timerGo = False
         # Show all the tiles and update view
         self.game.showAll()
         self.setButtons()
         
         # Detect endgame state
         if self.game.isExploded():
            text = "You lost!"
            self.emote["image"] = self.images["L"]
         else:
            text = f"You won!\nFinal time: {self.formatTime()}"
            self.emote["image"] = self.images["W"]
            
         self.messageBox("Game Is Over!", text)
         
         # Disable movement buttons and enable new game button
         for buttonRow in self.boardButtons:
            for b in buttonRow:
               b["state"] = "disabled"
         self.newGameButton["state"] = "normal"

   def newGame(self):
      """Create a new minesweeper game and updates the view."""
      self.game = Minesweeper(size=self.size, mines=self.mines)
      self.timer = 0
      self.timerLabel["text"] = f"Time: {self.formatTime()}"
      self.setButtons()  
      self.emote["image"] = self.images["."]
      
      # Enable movement buttons and disable new game button
      self.newGameButton["state"] = "disabled"      
      for buttonRow in self.boardButtons:
         for b in buttonRow:
            b["state"] = "normal"
      

def main():
   app = MinesweeperGUI()
   app.mainloop()
   
   app.timerGo = False

if __name__ == "__main__":
   main()
