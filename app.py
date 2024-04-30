"""
A Flask application for displaying soccer player information and statistics.

This application allows users to select a soccer league and either search for
a specific player or view the top players in a selected position. It utilizes 
the Player and PlayerLibrary classes from the DataStructure module to fetch 
and manage player data.

Routes:
- '/': Renders the main page with a form to select a league, the position or
       the player name.
- '/players': Handles form submissions, fetches player data, and renders player
              information or position rankings.

Functions:
- index(): Renders the main page with a form to select a league, the position or
           the player name.
- players(): Handles form submissions, fetches player data, and renders player
             information or position rankings.

Dependencies:
- Flask: A micro web framework for Python.
- DataStructure: Module containing the Player and PlayerLibrary classes for
                 managing soccer player data.

Usage:
- Run the application by executing this script.
- Access the application in a web browser by navigating to http://localhost:5000/.
- Select a league, enter a player name or choose a position, and submit the form
  to view player information.

Note: Ensure that the DataStructure module is properly configured and contains the
      necessary Player and PlayerLibrary classes.
"""


from DataStructure import Player, PlayerLibrary
from pathlib import Path
from flask import Flask, render_template, request
from jinja2 import Template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/players', methods=['POST'])
def players():
    league_dic = {'England': 39,
                  'Spain': 140,
                  'Italy': 135,
                  'Germany': 78,
                  'France': 61}
    
    
    country = request.form.get("country")
    name = request.form.get("name").strip()
    position = request.form.get("position")

    if not country:
        sentence = 'Please select the league you are interested in!'
        return render_template('warning.html', sentence=sentence)

    file = Path(country + '.json')
    if file.is_file():
        player_library = PlayerLibrary(file)
    else:
        player_library = PlayerLibrary()
        player_library.fetchPlayer(league_dic[country], 2023)
        player_library.cacheData(file)

    if name:
        if name not in player_library.playerNameList():
            sentence = 'This player is not in this league, please try another name!'
            return render_template('warning.html', sentence=sentence)
        else:
            return render_template('players.html', 
                                    dictionary=player_library.playerInfo(name),
                                    list_items=player_library.topTenSimilarPlayers(name),
                                    enumerate=enumerate)

    if position:
        players_list = [(player.name, player.rating) for player in player_library.positionList(position)[:10]]
        return render_template('positions.html', 
                                position = position,
                                list_items=players_list,
                                enumerate=enumerate)

    else:
        sentence = "Please select the position or type the player's name you are interested in!"
        return render_template('warning.html', sentence=sentence)
    

if __name__ == '__main__':
    print('starting flask app', app.name)
    app.run(debug=True)