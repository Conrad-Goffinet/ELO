# Notes: A Player's score is the number of cups they sink in one game


class Game:
    def __init__(self, team1, team2):
        # Teams are structured ((player1, score), (player2, score))
        print(team1, team2)
        self.team1 = team1
        self.team2 = team2
        self.winner = team1
        self.loser = team2
        self.participants_tup = team1 + team2
        self.player_stats = self.create_player_stats()
        self.players = (team1[0][0], team1[1][0], team2[0][0], team2[1][0])
        
        
    def create_player_stats(self):
        '''Returns a dict matching player names to a tuple of:
        (Score, Won (T/F), averaged PELO of opponents, opp_score)'''
        return_dict = {}
        for i, player_tup in enumerate(self.participants_tup):
            # Player tup is in the form of (<Player>, Score)
            if i < 2:
                won = True
                opp_elo = self.compute_team_pelo(self.team2)
                opp_score = self.team2[0][1] + self.team2[1][1]
                return_dict[player_tup[0].name] = (player_tup[1], won, opp_elo, opp_score)
            else:
                won = False  
                opp_elo = self.compute_team_pelo(self.team1)
                opp_score = self.team1[0][1] + self.team1[1][1]
                return_dict[player_tup[0].name] = (player_tup[1], won, opp_elo, opp_score)

        return return_dict

    def get_player_stats(self, player):
        return self.player_stats[player]
    
    def compute_team_pelo(self, team):         
        '''Computes the PELO of a team. Currently
        uses mean weighted toward better player'''
        upper_weight = .75 # Weight of better player
        better = max((team[0][0].get_pelo(), team[1][0].get_pelo()))*upper_weight
        worse = min((team[0][0].get_pelo(), team[1][0].get_pelo()))*(1-upper_weight)

        return better + worse
    

class Player:
    def __init__(self, name):
        self.name = name
        self.pelo = 500
        self.wins = 0
        self.losses = 0
        self.gp = 0
        self.games = []
        self.pelo_history = [500]
        self.mov_history = []
        self.avg_mov = 0
        self.score_history = []
        self.avg_score = 0 

    def play_game(self, game):
        self.games.append(game)
        # Stats = (Score, Won (T/F), averaged PELO of opponents, opp_score)
        stats = game.get_player_stats(self.name)
        if stats[1]:
            self.wins += 1
            self.mov_history.append(10-stats[3])
        else:
            self.losses += 1
            self.mov_history.append(stats[3]-10)
        
        self.gp += 1
        self.score_history.append(stats[0])
        self.update_score()
        self.update_pelo(*stats[0:3])
        self.update_mov()
    
    def get_pelo(self):
        return self.pelo

    def update_pelo(self, cups_for, won, opp_pelo):
        if won:
            k = 5 * cups_for
        else:
            k = 50 - (5* cups_for) # K is an elo parameter. The greater it is,
                                   # the more heavily a player's elo gets updated
         
        expected_value = 1 / (1 + 10 ** ((opp_pelo-self.get_pelo())/400)) # From wikipedia

        self.pelo += k * (won - expected_value)
        self.pelo_history.append(self.pelo)

    def update_mov(self):
        self.avg_mov = sum(self.mov_history)/len(self.mov_history)

    def update_score(self):
        self.avg_score = sum(self.score_history)/len(self.score_history)

    def get_statistics(self):
        return (self.name, self.wins, self.losses, self.gp, self.pelo, self.avg_mov, self.avg_score)

    def get_statistics_names(self):
        return ('Name', 'Wins', 'Losses', 'Games Played', 'PELO', 'Avg MOV', 'Avg Score')

class Database:
    def __init__(self):
        self.players = []
        self.games = []

    def get_players(self):
        return self.players

    def add_player(self, Player):
        self.players.append(Player)

    def get_games(self):
        return self.games

    def add_game(self, Game):
        self.games.append(Game)
        for player in Game.players:
            player.play_game(Game)

    def fetch_player(self, name):
        for player in self.players:
            if player.name == name:
                return player
        
            
    def create_player_name_list(self):
        '''Creates a list of names from a list of player
        objects'''
        return [player.name for player in self.players]

