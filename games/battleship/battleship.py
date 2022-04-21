from time import sleep

player1 = input("Player 1: ")
player2 = input("Player 2: ")
players = [player1, player2]
player_data = {}

def check_map(map): #check map
    n = []
    for i in range(len(map)):
        s = sum(map[i])
        n.append(s)
    return sum(n)

def create_map(player):
    player_map = [[],[],[],[]] #Map
    print(f"Make Map {player}")
    for row in range(len(player_map)):
        raw_string = input(f"Row {row+1}: ") #Row Input
        player_map[row] = raw_string.split(' ') #Split Input to List
        for column in range(len(player_map[row])):
            player_map[row][column] = int(player_map[row][column]) # Convert string list to integer list

    player_data[player] = {"map":player_map, "turns":0, "hits":0}

def play_battleship(attacker, defender):
    hits = player_data[attacker]["hits"]
    turns = player_data[attacker]["turns"]
    map = player_data[defender]["map"]
    while hits < 4:
        row = int(input(f"Choose Co-ordinates {attacker}\nRow (between 1 and 4): "))
        column = int(input("Column (between 1 & 4): "))
        if map[row-1][column-1] == 1:
            hits += 1
            map[row-1][column-1] = 0
            print(f'HIT! You have hit {hits} ships\nRemaining {4-hits} ships')
        else:
            print('Miss')
        turns += 1
        player_data[attacker]["turns"] = turns
    print(f'{attacker} took {turns} turns to beat the game')

def main():
    for player in players:
        create_map(player)
    play_battleship(players[0], players[1])
    play_battleship(players[1], players[0])
    turns = {}
    for player in players:
        turns.update({player:player_data[player]["turns"]})
    print(player_data)
    print(turns)
    max_chances = max(turns[players[0]], turns[players[1]])
    least_chances = min(turns[players[0]], turns[players[1]])
    winner = list(turns.keys())[list(turns.values()).index(least_chances)]
    print(f"{winner} won the game!!! By {max_chances-least_chances} chances!")
sleep(5)

if __name__ == '__main__':
    main()