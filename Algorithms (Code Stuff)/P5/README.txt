README

Heuristic: Prioritize crafting over collection with a clause for de-prioritizing pickaxe creation if the required pickaxe has a lower cost than the created pickaxe. 

Search: Looping until the time limit is reached, we perform a goal-regression (backwards) search that deconstructs the recipes in reverse. 
We first perform variable initialization for paths through the tree and costs of recipes. 
Then, we find all possible options for required items in the graph's state, building up a heap as we go. 
Popping from the queue we store the cost, state, and action of the state. Once the queue is empty of the current state is the goal, we attempt to iterate back to the top, [(None, None)]. 

Most Difficult Goal:
"furnace_minecart": 1,
"powered_rail": 20,
"rail": 50

Team:
Eric Shen   (eshen3)
Alex Cooper (maalcoop)