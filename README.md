# Binairo
For a side project, I have decided to try and implement a small game called Binairo. 

I was playing the games section on Linkedin, and on the site there is a puzzle game called Tango. Tango is super simple. 

You have a square grid of rows and columns, and we have 2 objects - a nought (O) or a cross (X).

The aim of the game is to have an even number of noughts and crosses in each row and column. 

We have some constraints to follow: 

1. We are not allowed more than 2 adjacent objects in a row or column. For example, OOX is valid, but OOO is invalid.
2. The opposite symbol (/) means that 2 adjacent objects are opposite to each other. E.g. if a puzzle had the combination O/, then we know that the next object is a cross -> O/X
3. The equals symbol (=) means that 2 adjacent objects will be the same as each other. E.g. if a puzzle had the combination O=, then we know that the next object is a cross -> O=O

These are the main rules for this game. I will be trying to implement it in the upcoming weeks.


JSON

"puzzle1" link - https://www.puzzle-binairo.com/binairo-plus-6x6-easy/

In the JSON file, there are 3 grids: 

1. The grid with just the 2 symbols.
2. Horizontal constraints.
3. Vertical constraints.

For grids 2, and 3, it tells you the relationships between two cells in the same row or column.

For example, if we had a row [".", "1", ".", "."] and a horizontal constraint of ["x", ".", "="]

then between (0,0) and (0,1) -> x (opposite)
     between (0,1) and (0,2) -> . (no constraint)
     between (0,2) and (0,3) -> = (equals)

and therefore it looks like this: 

Row 0 : [.] -x- [1] -.- [.] -=- [.] 
The total number of horizontal and vertical constraints is (n-1), where n is the size of the column or grid. 