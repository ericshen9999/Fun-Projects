#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    # Winning Strategy
    winning_sequence = Sequence(name='Largest Generation Strategy')

    # Check for largest generation and no neutral planets
    largest_generation_check = Check(have_largest_generation)
    neutral_check = Check(if_no_neutral_planet_available)

    # Find best attack strategy
    percentage_of_fleet = Selector('Find best attack Strategy')

    # If you have biggest fleet
    attack_sequence_allout = Sequence(name='Allout Attack Sequence')            # Start of Sequence
    largest_fleet_check = Check(have_largest_fleet)                             # Check largest fleet
    attack_selection_allout = Selector(name='Allout Attack Selection')          # Select attack stategy
    attack_weakest = Action(attack_weakest_enemy_planet)                        # One planet attack
    attack_all_weakest_enemy = Action(attack_all_weakest_enemy_planet)          # All planet attack
    attack_selection_allout.child_nodes = [attack_weakest, \
        attack_all_weakest_enemy]                                               # Add selector children nodes
    attack_sequence_allout.child_nodes = \
        [largest_fleet_check, attack_selection_allout]                          # Add sequence children nodes

    # If you have 75% of enemy fleet
    attack_sequence_75 = Sequence(name = '75% Attack Sequence')                 # Start of Sequence
    percent_75_check = Check(have_75_percent)                                   # Check 75% of enemy fleet
    attack_sequence_75.child_nodes = [percent_75_check, \
        attack_all_weakest_enemy.copy()]                                        # Add sequence children nodes

    percentage_of_fleet.child_nodes = \
        [attack_sequence_allout, attack_sequence_75]        # Add selector children nodes
    winning_sequence.child_nodes = \
        [largest_generation_check, neutral_check, percentage_of_fleet]          # Add sequence children nodes

    #Defend Strategy
    defend_sequence = Sequence(name='Defend Ally Sequence')                     # Start of Sequence (will always return False)
    defend_check = Check(cant_defend)
    defend_action = Action(defend_my_planet)                                    # Attempt to defend ally
    defend_sequence.child_nodes = [defend_check, defend_action]                 # Add sequence children nodes

    #Spread Strategy
    spread_sequence = Sequence(name='Spread Sequence')                          # Start of Sequence
    spread_action = Action(spread_to_best_production_planet)                    # Spread to neutral planet
    spread_sequence.child_nodes = [spread_action]                               # Add sequence children nodes

    # #Default Strategy
    # default_selector = Selector(name='Default Selector')                        # Start of Selector
    # neutral_sequence = Sequence(name='Neutral Sequence')                        # Start of Sequence
    # neutral_check = Check(if_neutral_planet_available)                          # Check if neutral planet avaliable
    # attack_all_neutral_action = Action(attack_all_weakest_neutral)              # Attack the weakest neutral with 10% of fleet
    # neutral_sequence.child_nodes = [neutral_check, attack_all_neutral_action]   # Add sequence children nodes
    attack_all_closest_all_action = Action(attack_all_closest_all)                # Attack the weakest planet avaliable
    # default_selector.child_nodes = [neutral_sequence, attack_all_weakest_action]# Add selector children nodes
    #Base
    root.child_nodes = [defend_sequence, winning_sequence, spread_sequence\
        , attack_all_closest_all_action]                                                     # Add sequence childre nodes

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
