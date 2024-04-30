Data Source: Soccer Player Data from API

Origin:
- URL for data: https://v3.football.api-sports.io
- Documentation: https://www.api-football.com/documentation-v3

Format(s):
- JSON: The player data is retrieved in JSON format from the API.

Access Method and Caching:
- The data is accessed using the requests library in Python, making GET requests to the API endpoint.

- Five national soccer leagues will be provided to the user for choosing, England, Spain, Italy, Germany and France. With the chosen league name, the league id could be found in the API document. All the players' inforamtion can be fetched using league id and season via API https://v3.football.api-sports.io/players. 

- The endpoint 'players' of this API uses a pagination system with 20 results per page, so we will have to adapt our scripts or make a recursive function in order to get all the expected results. This API has a 100 visits/day and 10 visits/minute limit. So it's better to cache the data to local file for the further use.

- The player's information includes id, name, age, team, position, rating, stats(shots, goals, passes, tackles, duels, dribbles, fouls)

- Caching: 

1. Caching is implemented to store the retrieved player data locally in JSON format. This cached data is used to avoid making repeated API requests in future for the same league.
2. The local JSON file is named as selected_coutry.json.

Summary of Data:
The player's information is stored in the Player class objects.
For each Player class object, there are 7 attributes:
  1. id (int)
  2. name (str)
  3. age (int)
  4. team (str)
  5. position (str)
  6. rating (str)
  7. stats (dictionary)

All the players are stored in a PlayerLibrary class object.
For the PlayerLibrary class object, there are 2 attributes:
  1. players (list of Player objects)
  2. playersGraph (dictionary of dictionary to store the similarities between each palyers in a graph structure)