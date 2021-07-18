
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    """
    #Not empty
    while bool(node.child_nodes):
        #Make a default
        select = list(node.child_nodes.values())[0]
        action = list(node.child_nodes.keys())[0]
        #If select is not visisted, visit it
        if select.visits == 0:
            state = board.next_state(state, action)
            node = select
            continue
        selectMath = select.wins / select.visits + explore_faction * sqrt(log(node.visits)/select.visits)
        #Iterate through all child nodes
        for i in node.child_nodes:
            #If unvisisted select it
            if node.child_nodes[i].visits == 0:
                select = node.child_nodes[i]
                action = i
                break
            #If I am the player use my win rate, otherwise use loss/tie rate
            if board.current_player(state) == identity:
                winrate = node.child_nodes[i].wins / node.child_nodes[i].visits
            else:
                winrate = 1 - (node.child_nodes[i].wins / node.child_nodes[i].visits)
            iMath = winrate + explore_faction * sqrt(log(node.visits)/node.child_nodes[i].visits)
            #Do math to decide
            if iMath > selectMath:
                selectMath = iMath
                select = node.child_nodes[i]
                action = i
        #Move to new node
        state = board.next_state(state, action)
        node = select
    #If node has been visisted before
    if node.visits > 0:
        expand_leaf(node, board, state)
    #Rollout and backpropagate
    points = rollout(board, state)
    #Find if you won, otherwise count it as a loss (Ties are bad)
    if points[identity] == 1:
        winner = True
    else:
        winner = False
    backpropagate(node, winner)


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    """
    while bool(node.untried_actions): 
        #Select random action
        action = node.untried_actions[0]
        node.untried_actions.remove(action)

        #Create new node
        new_node = MCTSNode(parent = node, parent_action = action, action_list = board.legal_actions(board.next_state(state, action)))
        node.child_nodes[action] = new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The the points at the end of the game.
    """
    #Rollout
    while not board.is_ended(state):
        state = board.next_state(state, choice(board.legal_actions(state)))
    return board.points_values(state)

def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    #Backpropogate
    while node is not None:
        #Add a counter if needed for every other node
        if won:
            node.wins += 1
        node.visits += 1
        node = node.parent


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    #print()
    #print("Think")
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        traverse_nodes(node, board, sampled_game, identity_of_bot)
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.

    select = list(root_node.child_nodes.values())[0]
    action = list(root_node.child_nodes.keys())[0]
    #Iterate through all child nodes
    for i in root_node.child_nodes:
        if root_node.child_nodes[i].visits == 0:
            continue
        iMath = root_node.child_nodes[i].wins / root_node.child_nodes[i].visits

        selectMath = select.wins / select.visits
        #Do math to decide
        if iMath > selectMath:
            select = root_node.child_nodes[i]
            action = i

    return action