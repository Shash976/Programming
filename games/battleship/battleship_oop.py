class Player:
    players = []
    def __init__(self, name, map, id, turns, hits):
      self.id = id
      self.name = name
      self.map = map
      self.turns  = turns 
      self.hits = hits
      self.__class__.players.append(self)

    def get_player_by_turns(self, turns):
        players = self.__class__.players
        for player in players:
            if player.turns == turns:
                p = player
        return p

def create_map(player):
    player.map = [[],[],[],[]] #Map
    print(f"Make Map {player.name}")
    for row in range(len(player.map)):
        raw_string = input(f"Row {row+1}: ") #Row Input
        player.map[row] = raw_string.split(' ') #Split Input to List
        for column in range(len(player.map[row])):
            player.map[row][column] = int(player.map[row][column]) # Convert string list to integer list

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

def main():
    for id in range(2):
        player = Player(name=input(f"Player {id+1}: "), id=id, map = '', turns=0, hits=0) #Create Player
        create_map(player)
    players = Player.players
    for i in players:
        player = players[0]
        players.remove(player)
        play_battleship(player, players[0])
        players.append(player)
    max_chances = max(players[0].turns, players[1].turns)
    least_chances = min(players[0].turns, players[1].turns)
    winner = players[0].get_player_by_turns(least_chances)
    print(f"{winner.name} won the game!!! By {max_chances-least_chances} chances!")

if __name__ == "__main__":
    main()