from PyQt6.QtWidgets import *
from PyQt6.QtGui import * 
from PyQt6 import uic
from PyQt6 import QtCore

import sys, os
import random
import shelve


def follow_me(num_of_steps): # Generate a random pattern, return list of steps in pattern.
    steps = []

    for x in range(num_of_steps):
        step = random.randint(1,4)
        steps.append(step)
    return steps


class window(QMainWindow): # Not very good at using classes. No clue why any of this works.
    switch = True
    flash_counter = 0
    color_counter = 1
    speed = 500
    pressCounter = 0
    score = 0
    current_level = 0
    best = 0
    already = False

    def __init__(self):
        super(window, self).__init__()
        ui_loc = os.path.realpath(__file__)
        ui_loc = (ui_loc.rsplit("\\", 1))[0] # Getting path of script, popping 'script.py' and adding ui filename.
        ui_loc = ui_loc+"\\simon.ui"
        uic.loadUi(ui_loc, self)
        window.reset(self)

        self.red = self.main.findChild(QPushButton, 'red')
        self.red.clicked.connect(self.game_buttonPressed)
        
        self.blue = self.main.findChild(QPushButton, 'blue')
        self.blue.clicked.connect(self.game_buttonPressed)
        
        self.green = self.main.findChild(QPushButton, 'green')
        self.green.clicked.connect(self.game_buttonPressed)
        
        self.yellow = self.main.findChild(QPushButton, 'yellow')
        self.yellow.clicked.connect(self.game_buttonPressed)

        self.current_score = self.main.findChild(QLCDNumber, 'cur_score')
        self.best_score = self.main.findChild(QLCDNumber, 'best_score')
        self.level = self.main.findChild(QTextEdit, 'level')

    def open_scoreboard(self, scores):
        self.leaderboard = self.scores.findChild(QTableWidget, 'leaderboard')
        all_scores = scores
        row = 0

        for x in range(len(scores)): # Sort every score in txt by highest to lowest - Separate the
                                     # -- first value's name and score, post to board element then 
                                     # ---  pop it and repeat for next highest value.
            all_scores.sort(key=lambda x: x[1], reverse=True)
            name = (all_scores[0])[0]
            points = (all_scores[0])[1]
            toggle = 0
            self.leaderboard.setItem(row, toggle, QTableWidgetItem(name)) # Values need to be saved as special 'QTableWidgetItem' objects to be posted properly.
            
            toggle ^= 1 # Using a xor toggle to easily switch between 0 and 1 for the two columns.
            self.leaderboard.setItem(row, toggle, QTableWidgetItem(str(points)))
            row += 1
            all_scores.pop(0)

    def reset(self): # Reset all in-use values and elements for the next game.
        window.steps = []
        window.switch = True
        window.flash_counter = 0
        window.color_counter = 1
        window.speed = 500
        window.pressCounter = 0
        window.score = 0
        window.current_level = 0

        self.tab_widget = self.findChild(QTabWidget, 'tabs')
        self.tab_widget.setCurrentIndex(0)
        self.main = self.tab_widget.findChild(QWidget, 'main')
        self.scores = self.tab_widget.findChild(QWidget, 'scores')
        
        self.difficulty = self.main.findChild(QComboBox, 'difficulty_selector')
        self.difficulty.activated.connect(lambda: self.pattern(no_reset=False))

        self.red.setEnabled(False)
        self.blue.setEnabled(False)
        self.green.setEnabled(False)
        self.yellow.setEnabled(False)
        self.difficulty.setDisabled(False)
        self.scoreboard(cond=2) # Call scoreboard to update the board.

    def scoreboard(self, cond):
        scores_loc = os.path.realpath(__file__)
        scores_loc = (scores_loc.rsplit("\\", 1))[0] # Get script path, drop the .py script, attach simon_scores, use as file path.
        scores_loc = scores_loc+"\\simon_scores"
        scores = shelve.open(scores_loc)
        
        all_scores = []
        username = self.main.findChild(QTextEdit, 'username').toPlainText().lower()
        scoreboard = dict(scores.items())
        
        if cond == 2:
            users = list(scoreboard)
            points = list(scoreboard.values())
            if len(points) > 0:
                window.best = 0
                for i,x in enumerate(users):
                    for p in points[i]:
                        user_point_pair = (x,p)
                        all_scores.append(user_point_pair)
                all_scores.sort(key=lambda x: x[1], reverse=True)
                self.best = (all_scores[0])[1]
                self.best_score.display(self.best)
                self.open_scoreboard(all_scores)

        elif username == "": # If username value is blank, their score will not be saved.
            None
        elif cond == True and window.score != 0: # If won, and score is not zero, save score and username in .txt file.
            if username in scoreboard:
                user_scores = list(scoreboard[username])
                user_scores.append(window.score)
                pass_score = {f"{username}": user_scores}
            else:
                pass_score = {f"{username}": [window.score]}
            scores.update(pass_score)
                
        scores.close()

    def change_color(self, win_state):
        flash_or_revert = window.switch

        if win_state == True: # If winning, flash the color green across all push buttons.
            if flash_or_revert == True:
                self.red.setStyleSheet('background-color : rgb(39, 171, 0)')
                self.blue.setStyleSheet('background-color : rgb(39, 171, 0)')
                self.green.setStyleSheet('background-color : rgb(39, 171, 0)')
                self.yellow.setStyleSheet('background-color : rgb(39, 171, 0)')
            elif flash_or_revert == False:
                self.red.setStyleSheet('background-color : rgb(141, 0, 2)')
                self.blue.setStyleSheet('background-color : rgb(0, 7, 150)')
                self.green.setStyleSheet('background-color : rgb(19, 131, 0)')
                self.yellow.setStyleSheet('background-color : rgb(164, 166, 12)')
                if window.flash_counter == 1:
                    self.timer.stop() # After a few flashes, stop timer.
            window.switch = not window.switch
            window.flash_counter += 1

        elif win_state == False: # If losing, flash the color red across all push buttons.
            if flash_or_revert == True:
                self.red.setStyleSheet('background-color : rgb(255, 0, 0)')
                self.blue.setStyleSheet('background-color : rgb(255, 0, 0)')
                self.green.setStyleSheet('background-color : rgb(255, 0, 0)')
                self.yellow.setStyleSheet('background-color : rgb(255, 0, 0)')
            elif flash_or_revert == False:
                self.red.setStyleSheet('background-color : rgb(141, 0, 2)')
                self.blue.setStyleSheet('background-color : rgb(0, 7, 150)')
                self.green.setStyleSheet('background-color : rgb(19, 131, 0)')
                self.yellow.setStyleSheet('background-color : rgb(164, 166, 12)')
                if window.flash_counter == 5:
                    self.timer.stop() # After a few flashes, stop timer.
            window.switch = not window.switch
            window.flash_counter += 1
            
        else: # If not winning or losing, new pattern is being shown. Flash colors brighter than the current on each step.
            step = window.steps[window.flash_counter]

            if flash_or_revert == True:
                if step == 1:
                    self.red.setStyleSheet('background-color : rgb(220, 0, 0)')
                elif step == 2:
                    self.blue.setStyleSheet('background-color : rgb(0, 3, 211)')
                elif step == 3:
                    self.green.setStyleSheet('background-color : rgb(0, 206, 6)')
                else:
                    self.yellow.setStyleSheet('background-color : rgb(225, 225, 0)')

            elif flash_or_revert == False:
                if step == 1:
                    self.red.setStyleSheet('background-color : rgb(141, 0, 2)')
                elif step == 2:
                    self.blue.setStyleSheet('background-color : rgb(0, 7, 150)')
                elif step == 3:
                    self.green.setStyleSheet('background-color : rgb(19, 131, 0)')
                else:
                    self.yellow.setStyleSheet('background-color : rgb(164, 166, 12)')
                if window.flash_counter == len(window.steps)-1:
                    self.timer.stop()
                    self.red.setEnabled(True)
                    self.blue.setEnabled(True)
                    self.green.setEnabled(True)
                    self.yellow.setEnabled(True)

            window.switch = not window.switch
            if window.color_counter % 2 == 0:
                window.flash_counter += 1
            window.color_counter += 1

    def light_up(self):
        window.switch = True
        window.flash_counter = 0
        window.color_counter = 1
        self.steps = window.steps

        self.timer = QtCore.QTimer(self, interval=window.speed)
        self.timer.timeout.connect(lambda: self.change_color(win_state=2))
        self.timer.start()

    def pattern(self, no_reset):
        if self.difficulty.currentText() != "Difficulty":
            if no_reset == False:
                self.current_score.display(0)
            else:
                window.pressCounter = 0
                self.red.setEnabled(False)
                self.blue.setEnabled(False)
                self.green.setEnabled(False)
                self.yellow.setEnabled(False)

            difficulty = self.difficulty.currentText()
            number_of_steps = random.randint(2,5)
            self.difficulty.setDisabled(True)
            if difficulty == 'Easy':
                window.speed = 500
                window.steps += follow_me(number_of_steps)
                self.light_up()
            elif difficulty == 'Medium':
                window.speed = 350
                window.steps += follow_me(number_of_steps)
                self.light_up()
            elif difficulty == 'Hard':
                window.speed = 250
                window.steps += follow_me(number_of_steps)
                self.light_up()
        print(window.steps)

    def game_buttonPressed(self):
        window.pressCounter += 1
        self.u_steps = []

        if str(self.sender().objectName()) == "red":
            user_step = 1
        elif str(self.sender().objectName()) == "blue":
            user_step = 2
        elif str(self.sender().objectName()) == "green":
            user_step = 3
        elif str(self.sender().objectName()) == "yellow":
            user_step = 4
        self.u_steps.append(user_step)

        for x in range(len(self.u_steps)):
            if self.u_steps[0] != window.steps[window.pressCounter-1]: # LOST
                window.flash_counter=0
                self.timer = QtCore.QTimer(self, interval=window.speed)
                self.timer.timeout.connect(lambda: self.change_color(win_state=False))
                self.timer.start()
                
                self.difficulty.disconnect()
                self.difficulty.setCurrentIndex(0)
                window.scoreboard(cond=True)
                window.reset()
                break
            else: # IF YOU HAVEN'T LOST, POP INDEX OFF
                window.score += 5

                if window.score > window.best: # If you have the new high score, display current score in best score and flash all tiles green for 150 ms
                    self.best_score.display(window.score)

                    '''if not window.already: ### Not sure if I want this kept in. Might be distracting if the tiles flash green mid-round.
                        window.flash_counter = 0
                        self.timer = QtCore.QTimer(self, interval=150)
                        self.timer.timeout.connect(lambda: self.change_color(win_state=True))
                        self.timer.start()
                        window.already = True ###'''

                self.current_score.display(window.score)
                self.u_steps.pop(0)
            if len(self.u_steps) == 0 and window.pressCounter == len(window.steps): # IF YOU HAVEN'T LOST, AND YOU HAVE DONE THE SAME AMOUNT OF STEPS AS IN PATTERN, ADD TO LEVEL SCORE
                self.current_level+=1
                level_text = "Level: " + str(self.current_level)
                self.level.setProperty("placeholderText", level_text)

                self.pattern(no_reset=True)
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = window()
    window.setWindowFlags(window.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint) # Trying to get window to raise on start up, 
    window.setWindowFlags(window.windowFlags() & ~QtCore.Qt.WindowType.WindowStaysOnTopHint)#- it keeps opening in background for me.
    window.show() # All windows start vanished.
    app.exec()