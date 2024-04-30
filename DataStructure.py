import requests
import json
import time

class Player:
    """
    A class representing a soccer player with attributes related to his
    demographic and statistics. The player's data is fetched from
    https://v3.football.api-sports.io.

    Parameters 
    ------------------------------
    id: int
        The unique identifier for the player.

    name: str
        The player's name in the format of "first_name, last_name"
    
    age: int
        The player's age

    team: str
        The player's team

    position: str
        The player's position (Goalkeeper, Defender, Midfielder, Attacker)

    rating: str
        The player's performence rating in the whole seaon. Could be 'null'
        if this player didn't play any game in the whole season.

    stats: dictionary
        The player's key performence statistics inclduing shots, goals,
        passes, tackles, duels, dribbles, fouls

    Attributes
    ------------------------------
    self.id = id
    self.name = name
    self.age = age
    self.team = team
    self.position = position
    self.rating = rating
    self.stats = stats

    """
    def __init__(self, id, name, age, team, position, rating, stats):
        self.id = id
        self.name = name
        self.age = age
        self.team = team
        self.position = position
        self.rating = rating
        self.stats = stats


class PlayerLibrary:
    '''
    A class to include all soccer players in a soccer league and
    compare two players in the network of players.

    Attributes
    ------------------------------
    self.players: a list of Player object
        collect all players' data

    Methods
    ------------------------------
    fetchPlayer(league_id, season):
        fetches the players data for perticular league for perticular season

    cacheData(fileName):
        save the current state of players data to a file in JSON format

    loadCache(fileName):
        load players data from a cache JSON file if it exists.
    
    '''
    def __init__(self, cacheFile = None):
        """
        Initialize the PlayerLibrary class with an empty players list. Import
        players data from cache file if cache file is given.

        Parameters 
        ------------------------------
        cacheFile: str
            The file to store the cached players data
        """
        print('PlayerLibrary starts')
        self.players = []
        if cacheFile:
            self.loadCache(cacheFile)
            print(f'Load data from {cacheFile}')

        self.playersGraph = {}
        self.generatePlayersGraph(self.players)


    def playerInfo(self, name):
        """
        Retrun the player's information based on the provided name.

        Parameters 
        ------------------------------
        name: str
            The player's name.

        Returns
        -------
        dictionary
            player's information
        """
        for player in self.players:
            if player.name == name:
                return player.__dict__
            
        return None


    def playerNameList(self):
        """
        Retrun all the player's name in the current dataset.

        Parameters 
        ------------------------------

        Returns
        -------
        list
            all the player's name
        """
        return [player.name for player in self.players]
    
    
    def positionList(self, position):
        """
        Retrun all the players in the giving position, sorted by the rating.
        Four positions are: Goalkeeper, Defender, Midfielder, Attacker

        Parameters 
        ------------------------------
        position: str
            The position of players

        Returns
        -------
        list
            all the players in that position
        """
        return sorted([player for player in self.players if player.position == position],
                      key=lambda x: (x.rating is not None, x.rating),
                      reverse=True)


    def fetchPlayer(self, league_id, season):
        """
        Fetches the players data from https://v3.football.api-sports.io.
        This API allowes 10 requests per minute and 100 requests per day.

        Parameters 
        ------------------------------
        league_id: int
            The unique id of the soccer league. The unique id could be 
            found at https://dashboard.api-football.com/soccer/ids.
            Some common league's id:
            England Premier League: 39
            Spain La Liga: 140
            Italy Serie A: 135
            Germany Bundesliga: 78
            France Ligue 1: 61
            Netherlands Eredivisie: 88

        season: int
            The season which players played

        Returns
        -------
        None
        """
        base_url = 'https://v3.football.api-sports.io/players'
        payload = {'league':league_id, 'season':season, 'page':1}
        headers = {
            'x-rapidapi-key': 'access_key_from_v3.football.api',
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }

        stats_keys = ['shots', 'goals','passes', 'tackles', 'duels', 'dribbles', 'fouls']

        while True:
            response = requests.request("GET", base_url, headers=headers, params=payload)
            #print(payload['page'])
            #print(json.loads(response.text).get('response')[0]['player']['name'])
            data = json.loads(response.text)
            for d in data['response']:
                id = d['player']['id']
                name = d['player']['firstname'] + ', ' + d['player']['lastname']
                age = d['player']['age']
                team = d['statistics'][0]['team']['name']
                position = d['statistics'][0]['games']['position']
                rating = d['statistics'][0]['games']['rating']
                stats = {}
                for key in stats_keys:
                    stats[key] = d['statistics'][0][key]

                self.players.append(Player(id, name, age, team, position, rating, stats))

            data_page = data.get('paging')
            if data_page['current'] == data_page['total']:
                print(data_page['current'], data_page['total'])
                break
            payload['page'] += 1
            if payload['page']%10 == 0:
                print('sleep for 1 min')
                time.sleep(60)


    def cacheData(self, fileName):
        """
        Saves the current state of players data to a file in JSON format.
        Using the __dict__ magic method on each Player instance, and save the 
        result of it to a list.
        After creating the list, dump it to a json file with the inputted name.

        Parameters
        ----------
        filename : str
            The name of the file where the players data will be saved.
        """
        players_list = []
        for player in self.players:
            players_list.append(player.__dict__)

        with open(fileName, 'w') as file:
            json.dump(players_list, file)


    def loadCache(self, fileName):
        """
        Loads players data from a cache JSON file if it exists.

        Parameters
        ----------
        fileName : str
            The name of the file from which to load the players data.

        Returns
        -------
        bool
            True if the data was successfully loaded, False otherwise.
        """
        try:
            with open(fileName, 'r') as file:
                data = json.load(file)
            
            for d in data:
                self.players.append(Player(d['id'], 
                                           d['name'], 
                                           d['age'], 
                                           d['team'], 
                                           d['position'], 
                                           d['rating'], 
                                           d['stats']))
            return True
        except:
            return False


    def generatePlayersGraph(self, playerlist):
        """
        Generate a graph among all the players in the playerlist based on the similarity of each player's stats.
        The graph will be store as a dictionary of dictionary in the self.playersGraph attribute.

        Parameters
        ----------
        playerlist : list
            The list contains all the players.

        Returns
        -------
        None
        """

        stats_keys = ['shots', 'goals','passes', 'tackles', 'duels', 'dribbles', 'fouls']

        for key_player in playerlist:
            self.playersGraph[key_player.name] = {}
            for similar_player in playerlist:
                if similar_player.position == key_player.position and similar_player.name != key_player.name and similar_player.rating:
                    #print(key_player.stats)
                    #print(similar_player.stats)
                    for s in stats_keys:
                        for key in list(key_player.stats[s].keys()):
                            if key_player.stats[s][key] and similar_player.stats[s][key]:
                                if similar_player.name in self.playersGraph[key_player.name]:
                                    self.playersGraph[key_player.name][similar_player.name] += abs(key_player.stats[s][key] - similar_player.stats[s][key])
                                else:
                                    self.playersGraph[key_player.name][similar_player.name] = abs(key_player.stats[s][key] - similar_player.stats[s][key])


    def topTenSimilarPlayers(self, playername):
        """
        Select the top ten smililar players to the given player's name based on the self.playersGraph

        Parameters
        ----------
        playername : str
            The name of the player you are interested in

        Returns
        -------
        list of tuple
            A list of top 10 similar players with their name and similarity score.
        """
        similarPlayers = []
        for p in sorted(self.playersGraph[playername], key=self.playersGraph[playername].get)[:10]:
            similarPlayers.append((p, self.playersGraph[playername][p]))
        return similarPlayers


def main():
    #player_library = PlayerLibrary()
    #player_library.fetchPlayer(39, 2023)
    #player_library.cacheData("England.json")
    player_library = PlayerLibrary("England.json")
    for p in player_library.positionList('Attacker')[:10]:
        print(p.name, p.rating)
    print(player_library.playerInfo('Erling, Braut Haaland'))
    print(player_library.topTenSimilarPlayers('Erling, Braut Haaland'))


if __name__ == '__main__':
    main()