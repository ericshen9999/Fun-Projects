import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappop, heappush

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
        return self.__key() < other.__key()

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

        # If Consumes exists
        if 'Consumes' in rule:
            for con in rule['Consumes']:
                # If you find the matching item
                found = False
                for s in state:
                    if s == con and state[s] >= rule['Consumes'][con]:
                        found = True
                        break
                if found:
                    continue
                # Return false if item not found
                return False
        # If Requires exists
        if 'Requires' in rule:
            for req in rule['Requires']:
                # If you find the matching item
                found = False
                for s in state:
                    if s == req and state[s] >= rule['Requires'][req]:
                        found = True
                        break
                if found:
                    continue
                # Return false if item not found
                return False
        # If all items are found and greater then return
        return True

    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()
        # Consumes exists
        if 'Consumes' in rule:
            for con in rule['Consumes']:
                for i in state:
                    if i == con:
                        # Update the values
                        next_state[i] = next_state[i] - rule['Consumes'][con]
        # Produces exists
        if 'Produces' in rule:
            for pro in rule['Produces']:
                for i in state:
                    if i == pro:
                        # Update the values
                        next_state[i] = next_state[i] + rule['Produces'][pro]
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for s in state:
            for g in goal:
                if s == g and state[s] < goal[g]:
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


def heuristic(state, new_state):
    # Implement your heuristic here!
    if is_goal(new_state):
        return -10000
    onlyOne = ["bench", "wooden_pickaxe", "wooden_axe", "stone_axe", "stone_pickaxe", "iron_axe", "iron_pickaxe", "furnace"]
    for i in new_state:
        if i in onlyOne:
            if new_state[i] > 1:
                return 1000
            elif new_state[i] > state[i]:
                return -1000
    return 1

def search(graph, state, is_goal, limit, heuristic):

    start_time = time()

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state

    # Intiailze Variables
    cost = 0
    action = None
    # Map down the tree
    pathMap = {}
    pathMap[state] = (None, None)
    # Queue
    queue = []
    # Output
    output = []
    while time() - start_time < limit:
        # (name, new_state, cost)
        possible = graph(state)
        for i in possible:
            if i[1] not in pathMap.keys():
                pathMap[i[1]] = (state, i[0])
                # (queue, (cost, new_state, action, parent_state))
                heappush(queue, (cost + i[2] + heuristic(state, i[1]), i[1], i[0], state))
        # If finished
        if len(queue) == 0 or is_goal(state):
            temp = (state, action)
            while temp[0] != None:
                # If you hit none leave
                if pathMap[temp[0]][0] == None:
                    break
                # Update the list
                outputState = pathMap[temp[0]]
                output.append(outputState)
                temp = pathMap[temp[0]]
            return output
        # Get items from the queue
        pick = heappop(queue)
        cost = pick[0]
        state = pick[1]
        action = pick[2]

    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

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
    state.update(Crafting['Initial'])

    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 30, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)