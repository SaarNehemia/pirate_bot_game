# pirate_bot_game
pirate bot game (inspired by Skillz high school coding competition).
Develop a bot that moves ships across the board, capture islands and destroy enemy ships.

## Create venv

Write in Terminal:

    python -m venv ./venv

    venv\Scripts\activate.bat

    pip install -r requirements.txt

There you go - all set up.

## Create your bot
1. Create python file (.py) under "players" folder with your name (lower case and underscore for spaces).
2. Write the following:

 
    import classes.api as game_api

    class <Your script name in camel case>:

    def __init__(self):
        <Your init code here>
    
    def do_turn(self, game_api: game_api.API):
        <Your code to execute each turn here>



