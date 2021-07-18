import sys
import math
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # Find weakest enemy
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    # If weakest enemy doesn't exist
    if not weakest_planet:
        return False
    
    # Find closest ally
    cur_best_distance = 0
    cur_best_planet = None
    for j in state.my_planets():

        # Distance
        jMath = state.distance(j.ID, weakest_planet.ID)

        # Check if the planet has more than double (ships + generated ships)
        if j.num_ships > (weakest_planet.num_ships + jMath) * 2:
            if jMath < cur_best_distance:
                cur_best_distance = jMath
                cur_best_planet = j
    
    if not cur_best_planet:
        # No legal source or destination
        return False
    else:
        # Send enough to take the weakest planet
        return issue_order(state, cur_best_planet.ID, weakest_planet.ID, math.ceil((weakest_planet.num_ships + cur_best_distance) * 2))
    return False

def attack_all_weakest_enemy_planet(state):
    # Find weakest enemy
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    # If weakest enemy doesn't exist
    if not weakest_planet:
        return False
    
    # Send 10% of all ally ships
    check = True
    for j in state.my_planets():
        if j.num_ships > 1:
            check = issue_order(state, j.ID, weakest_planet.ID, math.ceil(j.num_ships * .1))
        # If any fail
        if check is False:
            return False
    # Attempt to always return true
    return True

def attack_all_closest_all(state):
    # Find closest planet
    best_distance = 0
    best_planet = None
    for i in state.not_my_planets():
        cur_distance = 0
        for j in state.my_planets():
            cur_distance += state.distance(j.ID, i.ID)
        if cur_distance > best_distance:
            best_distance = cur_distance
            best_planet = i

    # If weakest enemy doesn't exist
    if not best_planet:
        return False

    # Find incoming ships
    incoming_ships = 0
    for f in state.my_fleets():
        if f.destination_planet == best_planet.ID:
            incoming_ships += f.num_ships
    # If enough are found
    if incoming_ships > best_planet.num_ships:
        return False
    
    # Send 10% of all ally ships
    check = True
    for j in state.my_planets():
        if j.num_ships > 1 and incoming_ships <= best_planet.num_ships:
            check = issue_order(state, j.ID, best_planet.ID, math.ceil(j.num_ships * .1))
        # If any fail
        if check is False:
            return False
    # Attempt to always return true
    return True

def spread_to_best_production_planet(state):
    # Intialize
    best_production_planet = None
    my_best_planet = None
    my_best_ship = None
    bestMath = 0
    leave = False

    # Check all neutral planets
    for i in state.not_my_planets():
        # If a fleet is already headed there ignore it
        for f in state.my_fleets():
            if f.destination_planet == i.ID:
                leave = True
                break
        if leave:
            leave = False
            continue


        # Find the closest ally planet.
        cur_best_distance = None
        cur_best_planet = None
        cur_need_ship = None
        for j in state.my_planets():
            # Check if the planet has enough ships
            jMath = state.distance(j.ID, i.ID)
            shipMath = (i.num_ships + 5 + math.ceil(jMath * i.growth_rate)) * 1.1
            if j.num_ships > shipMath:
                if cur_best_distance == None or jMath < cur_best_distance:
                    cur_best_distance = jMath
                    cur_best_planet = j
                    cur_need_ship = shipMath

        # Formula to figure out if planet is the best       (Consider proximity to enemy)
        if i.num_ships == 0:
            iMath = i.growth_rate
        else:
            iMath = i.growth_rate / i.num_ships
        if iMath > bestMath:
            bestMath = iMath
            best_production_planet = i
            my_best_planet = cur_best_planet
            my_best_ship = cur_need_ship
    
    if not my_best_planet or not best_production_planet:
        # No legal source or destination
        return False
    else:
        # Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, my_best_planet.ID, \
            best_production_planet.ID, \
            math.ceil(my_best_ship))

def defend_my_planet (state):
    # Intialize
    leave = False
    defend_planet = None
    num_of_ships = 0
    incoming_ships = 0
    # Check for enemy fleets
    for i in state.enemy_fleets():
        # Find the planet being attacked
        for j in state.my_planets():
            if i.destination_planet == j.ID:
                # Check for ally fleets
                for s in state.my_fleets():
                    if s == j.ID:
                        incoming_ships += s.num_ships
                # If it cant defend on its own (this check can theoretically fail)
                if i.num_ships > j.num_ships + i.turns_remaining * j.growth_rate + incoming_ships:
                    defend_planet = j
                    # Send 110% of required ships
                    num_of_ships = (i.num_ships - (incoming_ships + (j.num_ships + i.turns_remaining * j.growth_rate))) * 1.1
                    leave = True
                    break
        if leave:
            break

    # Check if there is an issue
    if not defend_planet:
        return False
    
    # Check my planets
    cur_best_distance = 0
    cur_best_planet = state.my_planets()[0]
    for j in state.my_planets():
        # Check if the planet has enough ships
        if j.num_ships > num_of_ships:
            # Distance
            jMath = state.distance(j.ID, cur_best_planet.ID)
            if jMath > cur_best_distance:
                cur_best_distance = jMath
                cur_best_planet = j
    
    if not cur_best_planet:
        # Send nearest planet
        for k in state.my_planets():
            kMath = state.distance(k.ID, cur_best_planet.ID)
            # Find closest planet with more than 33% of needed ships
            if k.num_ships > (num_of_ships * 0.33) and kMath > cur_best_distance:
                cur_best_distance = kMath
                cur_best_planet = k
        # Send all of the closest source
        issue_order(state, cur_best_planet.ID, defend_planet.ID, cur_best_planet.num_ships)
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        issue_order(state, cur_best_planet.ID, defend_planet.ID, math.ceil(num_of_ships))
    return False

def do_nothing (state):
    return True
