import pandas as pd
import dash_html_components as html

def create_data_table(database):
    '''Creates a grand table of player data
    for display in the app'''
    data = []
    Players = database.get_players() 
    for player in Players:
        data.append(player.get_statistics())
    df = pd.DataFrame(data, columns = Players[0].get_statistics_names())
    df = df.sort_values(by = ['PELO'], ascending = False )
    df = df.round(decimals = 2)
    
    return df

def create_html_table(table):
    '''Creates an HTML table from a pandas
    dataframe'''
    # Header
    out = [html.Tr([html.Th(col) for col in table.columns])] 

    # Body
    out = out + [html.Tr([
        html.Td(table.iloc[i][col]) for col in table.columns
    ]) for i in range(len(table))]

    return out


def create_player_dropdown(database):
    '''Creates a list of dictionaries properly
    formatted for player selection'''
    out_list = []
    for player in database.get_players():
        out_list.append({'label':player.name, 'value':player.name})

    return out_list
