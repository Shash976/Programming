from time import sleep

player1 = input("Player 1: ")
player2 = input("Player 2: ")
players = [player1, player2]
player_data = {}

def create_player(player):
    player_map = [[],[],[],[]]
    print(f"Make Map {player}")
    for n in range(len(player_map)):
        raw_string = input(f"Row {n+1}: ")
        player_map[n] = raw_string.split(' ')
        for x in range(len(player_map[n])):
            player_map[n][x] = int(player_map[n][x])

    player_data[player] = {"map":player_map, "turns":0, "hits":0}


def game(attacker, defender):
    hits = player_data[attacker]["hits"]
    turns = player_data[attacker]["turns"]
    map = player_data[defender]["map"]
    while hits < 4:
        row = int(input(f"Choose Co-ordinates {attacker}\nRow (between 0 and 3): "))
        column = int(input("Column (between 0 & 3): "))
        if map[row][column] == 1:
            hits += 1
            map[row][column] = 0
            print(f'HIT! You have hit {hits} ships\nRemaining {4-hits} ships')
        else:
            print('Miss')
        turns += 1
        player_data[attacker]["turns"] = turns
    print(f'{attacker} took {turns} turns to beat the game')

for player in players:
    create_player(player)
game(players[0], players[1])
game(players[1], players[0])
turns = {}
print(player_data)
for player in players:
    turns.update({player:player_data[player]["turns"]})
print(player_data)
print(turns)
max_chances = max(turns[players[0]], turns[players[1]])
least_chances = min(turns[players[0]], turns[players[1]])
winner = list(turns.keys())[list(turns.values()).index(least_chances)]
print(f"{winner} won the game!!! By {max_chances-least_chances} chances!")
sleep(5)