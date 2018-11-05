from Game_and_Player import * 
from app_utilities import *
import pickle

user_input = None
data = pickle.load(open('data.p','rb'))

while user_input != 'exit':
    user_input = input('Type a command: ')
    input_list = user_input.lower().split()
    
    if input_list[0] == 'name': # if user wishes to add a name
        if input_list[1] == 'add':
            data.add_player(Player(input_list[2]))
            pickle.dump(data, open( "data.p", "wb" ))
        if input_list[1] == 'rm':
            data.remove_player(input_list[2])

    if input_list[0] == 'game':
        if input_list[1] == 'add':
            names = data.create_player_name_list()
            print('Here\'s a list of players', names)
            P1 = input('Winning Player 1 Name: ')
            P1_score = input('Player 1 score: ')
            P2 = input('Winning Player 2 Name: ')
            P2_score = input('Player 2 score: ')
            P3 = input('Losing Player 3 Name: ')
            P3_score = input('Player 3 score: ')
            P4 = input('Losing Player 4 Name: ')
            P4_score = input('Player 4 score: ')
            
            while P1 not in names:
                P1 = input('Oops! Player 1 is not a valid  name. Try again: ') 
            while P2 not in names:
                P2 = input('Oops! Player 2 is not a valid  name. Try again: ')
            while P3 not in names:
                P3 = input('Oops! Player 3 is not a valid  name. Try again: ')
            while P4 not in names:
                P4 = input('Oops! Player 4 is not a valid  name. Try again: ')

            if int(P1_score) + int(P2_score) != 10:
                P1_score = input('Oops! The scores of player 1 and 2 don\'t add up to 10! Player 1 score: ')
                P2_score = input('Player 2 score: ') 

            if int(P3_score) + int(P4_score) >= 10:
                P1_score = input('Oops! The scores of player 3 and 4 don\'t add up! Player 3 score: ')
                P2_score = input('Player 4 score: ') 

            confirmation = input('Winners: '+P1+':'+P1_score+', '+P2+':'+P2_score+',\n' +
                                 'Losers: '+P3+':'+P3_score+', ' +P4+':'+P4_score+'\n'
                                 'Is this correct? (y/n) ')
            if confirmation.lower() == 'y':
                team1 = ((data.fetch_player(P1), P1_score),(data.fetch_player(P2), P2_score))
                team2 = ((data.fetch_player(P3), P3_score),(data.fetch_player(P4), P4_score))

                game = Game(team1, team2)
                data.add_game(game)
                pickle.dump(data, open( "data.p", "wb" ))

            else: 
                continue

    if input_list[0] == 'exit':
        break

print('Goodbye!')


