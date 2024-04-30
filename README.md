# Soccer Player Information Web App

This Flask web application allows users to view information about soccer players based on various criteria such as country, player name, and player position.


# Usage
Five national soccer leagues will be provided to the user for choosing, England, Spain, Italy, Germany and France. With the chosen league name, the players' information for season 2023-2024 will be fetched from https://v3.football.api-sports.io via API request. The players data will be cached into a json file for the further use. Then all players will connect with the other players based on the similarity of their statistics in a graph structure. The node will be player and the edge is a similarity score of their statistics.

Then four positions are provided to the user for choosing, goalkeeper, defender, midfielder and attacker. With the chosen position, top 10 players with the highest rating will be present to the user. player's name, rank and rating will be displayed.

Lastly, user can input the full name of the player and get all the detailed information of that player, including id, name, age, team, position, rating and stats (shots, goals, passes, tackles, duels, dribbles and fouls). The app will also recommand the top 10 similar players based on their similarity score in the graph.

Warning Messages: If no country is selected or if the input position are incomplete or if the player doesn't exist in the selected league, warning messages are displayed.


# Getting Started
To run the application locally, follow these steps:

1. Prerequisites
Python 3.x installed on your system.
requests, flask and its dependencies installed. You can install them via pip:

pip install requests
pip install flask

2. Installation
Download these files to your local machine:
DataStructure.py
app.py
template folder contains four html files

3. Create an account at https://dashboard.api-football.com/soccer/ids
Fill the x-rapidapi-key in the DataStructure.py with the access key in your account.

4. Navigate to the project directory
cd to the working directory

5. Running the Application
Run the Flask application:
python app.py

6. Open your web browser and go to http://localhost:5000 to access the application.


# File Structure
app.py: The main Flask application file containing route definitions and logic.
main.html: HTML template for the home page.
players.html: HTML template for displaying player information.
positions.html: HTML template for displaying top players in a specific position.
warning.html: HTML template for displaying warning messages.
DataStructure.py: Python file containing the Player and PlayerLibrary classes.
country.json: JSON files containing player data for specific countries (generated after fetching data).


# Imrpovments:
1. The current app displays top 10 similar players or top 10 players for each position via clickable links. But when you click it, it doesn't redirect to the player's information. We can improve the app.py to implement this function.
2. Create base_template and reference it in other templates.
3. Improve the algorithm to calculate the edge between each nodes in the playersGraph graph structure. The current algorithm is calculating the sum of the differece of each statistics between two players. The sum, which is the similarity score, increases as the similarity between two players decreases. 


# Feel free to customize this README file further based on your project's specific requirements and additional functionalities!


