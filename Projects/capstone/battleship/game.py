from .models import *

def play_battleship(attacker, defender):
    attacker.hits = 0
    attacker.turns = 0
    while attacker.hits < 4:
        row = int(input(f"Choose Co-ordinates {attacker.name}\nRow (between 1 and 4): "))-1
        column = int(input("Column (between 1 & 4): "))-1
        if defender.map[row][column] == 1:
            attacker.hits += 1
            defender.map[row][column] = 0
            print(f'HIT! You have hit {attacker.hits} ships\nRemaining {4-attacker.hits} ships')
        else:
            print('Miss')
        attacker.turns += 1
    print(f'{attacker.name} took {attacker.turns} turns to destroy {defender.name}\'s fleet!!')