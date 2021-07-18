

def if_neutral_planet_available(state):
    if bool(state.neutral_planets):
      return True
    return False

def if_no_neutral_planet_available(state):
    if not bool(state.neutral_planets):
      return True
    return False

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > (sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())) \
               * 1.1

def have_75_percent(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > (sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())) \
               * 0.75

def have_50_percent(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > (sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())) \
               * 0.5

def less_50_percent(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           <= (sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())) \
               * 0.5

def have_largest_generation(state):
    return sum(planet.growth_rate for planet in state.my_planets()) \
      > sum(planet.growth_rate for planet in state.enemy_planets())

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def cant_defend(state):
    incoming_ships = 0
    for i in state.enemy_fleets():
        for j in state.my_planets():
            if i.destination_planet == j.ID:
                for s in state.my_fleets():
                    if s == j.ID:
                        incoming_ships += s.num_ships
                if i.num_ships > j.num_ships + i.turns_remaining * j.growth_rate + incoming_ships:
                  return True
    return False