# FinalProjectofPython
This program requires python3.6+, (ran in the 3.10 environment on my computer).
This program needs to run when connected to the network.
This program requires these packages: requests, json, flask, datetime. It also requires a secrets_keys.py which provide the API keys (import this file in the data_access_process.py).

Brief instructions for how to interact with this program:
1. Run the data_access_process.py.
2. Then click the url in the terminal, which will open a webpage in your browser.
3. Then you just need to click the options follow the instructions, and this program will give you some suggestions on when to eat and which restaurant you should go to eat at. 
4. You can click the "print the tree" to display the decision tree I built using the data from the APIs, which the program traversed to ask the questions and give the suggestions.
5. You can click the "back to home" when available or click the UM logo to go to the home page for a new round input and play.

How data is organized into data structure:
I built trees similar to those of Project2, which are decision trees. Basically, these trees I built are filters, they provide options for users, then show the information according to the users choice. 
