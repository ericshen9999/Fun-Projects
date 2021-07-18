import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappop, heappush

import time as sleep

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        for i in self:
            if i != 'required' and i != 'created':
                if self[i] > other[i]:
                    return False
        return True
        #return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items()))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].

        # If you can produce the item
        if 'Produces' in rule:
            for pro in rule['Produces']:
                for i in state:
                    if type(state[i]) == int and state[i] > 0 and i == pro:
                        return True
        return False
    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].

        # Make a new state
        next_state = state.copy()
        next_state['required'] = None
        # If recipe requires
        if 'Requires' in rule:
            for i in state:
                if i == list(rule['Requires'].keys())[0] and state[i] >= 0:
                    next_state['required'] = list(rule['Requires'].keys())[0]
        # If recipe consumes
        if 'Consumes' in rule:
            for con in rule['Consumes']:
                for i in state:
                    if i == con:
                        # Adds materials needed
                        next_state[i] = next_state[i] + rule['Consumes'][con]
        # If recipe produces
        if 'Produces' in rule:
            for pro in rule['Produces']:
                for i in state:
                    if i == pro:
                        # Reduce needed materials by created materials
                        next_state[i] = next_state[i] - rule['Produces'][pro]
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for i in state:
            # If it is an integer and greater than 0
            if type(state[i]) == int and state[i] > 0:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state):
    # Implement your heuristic here!
    return 0

def search(graph, state, is_goal, limit, heuristic, completed):

    start_time = time()

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state

    # If you already are finished
    if is_goal(state):
        return (None,None)
    # Initilaize lists
    output = []
    queue = []
    # Dictionary for the tree
    pathMap = {}
    pathMap[state] = (None, None)
    # Update state later
    addToState = state.copy()
    for s in addToState:
        if s != 'required' and s != 'created':
            addToState[s] = 0
    # Other variable initalization
    cost = 0
    action = None
    # Cost Dictionary
    costDictionary = {}
    costDictionary["bench"] = 6
    costDictionary["wooden_pickaxe"] = 12 + 6
    costDictionary["wooden_axe"] = 12 + 6
    costDictionary["furnace"] = 33 + 12 + 6
    costDictionary["stone_pickaxe"] = 9 + 12 + 6
    costDictionary["stone_axe"] = 9 + 12 + 6
    costDictionary["iron_pickaxe"] = 39 + 9 + 12 + 6
    costDictionary["iron_axe"] = 39 + 9 + 12 + 6
    # Loop until time limit
    operation = 0
    while time() - start_time < limit:
        operation += 1
        # Find all possible options
        possible = graph(state)
        for i in possible:
            # (queue, (cost, new_state, action, parent_state))
            if i[1]['required'] != None:
                requiredItem = i[1]['required']
            else:
                requiredItem = None
            # If path not already checked
            if i[1] not in pathMap.keys():
                costofrequired = 0 # Need to do this math
                # If there is an item you need to make
                if requiredItem != None:
                    # If there are no previously created (required) items
                    if i[1]['created'] == None:
                        i[1]['created'] = requiredItem
                    # If there are previously created (required) items
                    elif requiredItem not in i[1]['created']:
                        i[1]['created'] = i[1]['created'] + " " + requiredItem
                    costofrequired = costDictionary[requiredItem]
                # Add to the map and the queue                                 # Most changes happen here
                pathMap[i[1]] = (state, i[0])
                heappush(queue, (cost + i[2] + costofrequired, i[1], i[0], state))
        # If you finish
        if len(queue) == 0 or is_goal(state):
            # Attempt to iterate back to the top
            temp = (state, action)
            while temp[0] != None:
                # If you hit none leave
                if pathMap[temp[0]][0] == None:
                    break
                # Make a temp to create required items
                if temp[0]['required'] not in completed:
                    completed.append(temp[0]['required'])
                    # make an empty state with only required item
                    tempState = temp[0].copy()
                    for s in tempState:
                        if s == 'required' or s == 'created':
                            tempState[s] = None
                        else:
                            if s == temp[0]['required']:
                                tempState[s] = 1
                            else:
                                tempState[s] = 0
                    # Attempt to make the required item
                    updateList, createdItems = search(graph, tempState, is_goal, limit, heuristic, completed)
                    output = updateList + output
                # Update the list
                outputState = pathMap[temp[0]]
                output.insert(0,outputState)
                temp = pathMap[temp[0]]
            return output, temp[0]['created']
        # Pick from the queue
        pick = heappop(queue)
        cost = pick[0]
        state = pick[1]
        action = pick[2]
        #sleep.sleep(5)

        #update previous states with added items
    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return (None,None)

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    # print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    # print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    # print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})

    # Initalizes state with items you own as negative and items you need as positive    //Potential Change
    state.update(Crafting['Initial'])
    if len(state) > 0:
        for i in state:
            state[i] = state[i] * -1
    for item in Crafting['Goal']:
        for i in state:
            if i == item:
                state[i] = state[i] + Crafting['Goal'][item]
    #state.update(Crafting['Goal'])
    state['required'] = None
    state['created'] = None

    # Adding required items later
    completed = [None]

    # Search for a solution
    resulting_plan, useless = search(graph, state, is_goal, 5, heuristic,completed)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            #print('\t',state)
            print(action)
            pass
