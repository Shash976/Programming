class Player:
    def __init__(self, name, map, id, turns, hits):
        id = self.id
        name = self.name
        age = self.age

def create_map(player):
    player.map = [[],[],[],[]] #Map
    print(f"Make Map {player.name}")
    for row in range(len(player.map)):
        raw_string = input(f"Row {row+1}: ") #Row Input
        player.map[row] = raw_string.split(' ') #Split Input to List
        for column in range(len(player.map[row])):
            player.map[row][column] = int(player.map[row][column]) # Convert string list to integer list

def play_battleship(attacker, defender):
    while attacker.hits < 4:
        row = int(input(f"Choose Co-ordinates {attacker.name}\nRow (between 1 and 4): "))
        column = int(input("Column (between 1 & 4): "))
        if defender.map[row-1][column-1] == 1:
            attacker.hits += 1
            defender.map[row-1][column-1] = 0
            print(f'HIT! You have hit {attacker.hits} ships\nRemaining {4-attacker.hits} ships')
        else:
            print('Miss')
        attacker.turns += 1
    print(f'{attacker.name} took {attacker.turns} turns to destroy {defender.name}\'s fleet!!')

def main():
    players = []
    for id in range(2):
        player = Player
        player.id = id
        player.name = input(f"Player {id+1}: ")
        create_map(player)
        players.append(player)
    play_battleship(players[0], players[1])
    play_battleship(players[1], players[0])
    max_turns = max(players[0].turns, players[1].turns)
    min_turns = min(players[0].turns, players[1].turns)
    winner = max_turns - min_turns

if __name__ == "__main__":
    main()