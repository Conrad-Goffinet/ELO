import pandas as pd

def create_data_table(database):
    '''Creates a grand table of player data
    for display in the app'''
    data = []
    Players = database.get_players() 
    for player in Players:
        data.append(player.get_statistics())
    df = pd.DataFrame(data, columns = Players[0].get_statistics_names())
    df = df.sort_values(by = ['PELO'], ascending = False )
    
    return df


def create_player_dropdown(database):
    '''Creates a list of dictionaries properly
    formatted for player selection'''
    out_list = []
    for player in database.get_players():
        out_list.append({'label':player.name, 'value':player.name})

    return out_list
