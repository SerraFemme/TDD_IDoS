Copyright 2019, Russell Buckner, All rights reserved.

In Defense of Sieging

This is my first game, a turn based combat game that implements card game mechanics.

There is currently no installer as of yet, so the Requirements.txt will need to be
used by pip installer for the necessary modules.




Menu Controls:
-Up: Up Arrow Key or W
-Down: Down Arrow Key or S
-Left: Left Arrow Key or A
-Right: Right Arrow Key or D
-Select: Enter Key or E
-Back: Q (when applicable)

Battle Controls:
-Camera Up: Up Arrow Key
-Camera Down: Down Arrow Key
-Camera Left: Left Arrow Key
-Camera Right: Right Arrow Key
-Cursor Up: W
-Cursor Down: S
-Cursor Left: A
-Cursor Right: D
-Toggle Tile Info Bar: Tab
-Cycle Player Modes: Space Bar
-Select: Enter Key or E




Game Menus:
-Start Screen
--Press any key to progress to the Main Menu

-Main Menu
--Start: Proceeds to the Create Team Menu
--Exit: Terminates the program

-Create Team Menu:
--First Column: Class List
--Second Column: Player List
--Third Column: Proceed to Encounter Select Menu

-Encounter Select Menu:
--First Row: Tribe Select
---Press 'E' or Enter to Select Displayed Enemy Tribe
--Second Row: Displayed Difficulty
---Rest of the Column: Available encounters of the selected Tribe and the displayed
        difficulty

-Encounter Preview:
--Back: Go back to the Encounter Select Menu
--Start Battle: Begin battle phase

Battle Phase:
-In player turn order: select starting position
--Once a position has been selected, the starting position cannot be altered
-Once all players have selected their starting positions, then the game proceeds
        to the start of battle

Player Turn:
-Modes:
--Cursor: Display info of the highlighted tile, any effects on it, and info of
        the unit occupying it (Not yet implemented)
--Movement: Highlights adjacent tiles of the active player
---Yellow: available to move onto
---Red: Occupied, cannot be moved onto
---Grey: Insufficient stamina to move onto the tile
--Action:
---Hand: Displays cards in hand (Not yet implemented)
---Passive: Displays info, and buttons if available, of the player's class (Not yet implemented)
---Enchantments: Displays permanent cards affecting the player (Not yet implemented)
---Player Info: Displays tabs of various info screens about the player (Not yet implemented)
---End Turn: Passes turn to next player. Instead passes turn to enemy team if
        last player ends their turn.