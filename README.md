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
