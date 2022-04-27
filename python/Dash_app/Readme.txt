This document explains the technical setup of the dashboard. this folder has 
the following structure:

app.py --> Main file that runs the dashboard and creates the basic layout and
            updates the layout based on the current tab

Dataloading.py --> File containing cleaned datasets etc. ready for import.

assets folder --> Contains a css script to set the style of some parts of the 
dashboard Furthermore it contains all images used in the dashboard.

pages folder --> contains a .py file for each tab in the dashboard. the .py 
file is responsible for setting the layout for the tab and all callbacks
associated with the tab

info folder --> Contains all text files that is used in the dashboard. E.i
"Dice.txt" is the text file for information regarding the dice coefficient.