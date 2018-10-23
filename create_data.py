import pickle
import Game_and_Player as gp

player1 = gp.Player('Conrad')
player2 = gp.Player('Sweidman')
player3 = gp.Player('Ally')
player4 = gp.Player('Adriana')
db = gp.Database()
db.add_player(player1)
db.add_player(player2)
db.add_player(player3)
db.add_player(player4)

pickle.dump(db, open('data.p', 'wb'))