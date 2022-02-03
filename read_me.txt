simon.py is the (mostly) complete version of the program

simon-dev.py is identical, however, it prints the list for which button to press in console, so that if you want to (more easily) get through the game to see different features, you can. 

List example:
[1, 4, 3, 2] -> Red, Yellow, Green, Blue


Things that may not be intuitive:
	You can put your username in at any point before losing the round and it will save your score. If you do not put a username in before losing, it will not save the score. 
	
	The first LCD box is current_score, the second LCD box is best_score. When there is no best score, the current score is the best score (which is why they are the same value on first play-through.

	It's hard to see because the button colors are dark, but they ARE being clicked when you click. (except for when no difficulty has been selected, in that case I have the buttons disabled and they do not accept clicks.)

	The only difference between difficulties is speed at which it flashes the buttons.

	There is a tab at the top to see the leaderboard, it is not highly visible if you didn't know it exists.

	I was torn between adding patterns to the previous pattern to go on endlessly, and starting with an already long pattern to finish at a win_state when correctly completed. Some of the code (specifically in the change_color() function) reflects that. ("if win_state == True" will never be reached.)

	There is commented code in game_buttonPressed(), that was one idea I had for flashing the buttons quickly with green when the best_score is surpassed, but I felt it could be distracting if it happened mid-game, so I left it out for now.

	When first run, it will generate three simon_scores files. A .dat, .bak, and .dir file. From my understanding, these are generated due to the way that the shelve module was built, and it is to allow cross-platform compatibility and other functionality. Not sure if it is necessary for this particular program, but I didn't feel like messing around with it to see if I could use only one.