# About pirate_bot_game
pirate bot game (inspired by Skillz high school coding competition).

Develop a bot that moves ships across the board, capture islands and destroy enemy ships.

## Fork my repoistory
Follow this guide to fork and clone my repo: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo

### Notes

* You need to Download Git Bash.
* I recommend storing all your Git projects in one designated folder. Than, you can Open Git Bash in the folder by navigating to this folder using the file explorer and right click -> Open Git Bash Here. Alternatively, you can open Git Bash and change directory using the cd command (note you must use linux syntax, for example c:/users/saar.nehemia/projects).
* In the GitHub project site, Press code (green button) and copy HTTPS link to clone project to your local computer. You can also copy this link directly: https://github.com/SaarNehemia/pirate_bot_game.git
* write "git clone {paste HTTPS link}".
* There you go - project is saved on your local computer.
* (You can also use Git for Desktop to clone the project if you are familiar with it).

## Open Python IDE

Open project folder in your preferred python IDE (for example PyCharm).

### Create venv

Write in Terminal:

    python -m venv ./.venv

    .venv\Scripts\activate.bat

    pip install -r requirements.txt

There you go - all set up.

## Create your bot
1. Make sure to read Instructions document before starting developing your bot.
2. Create new branch for your bot development (main branch is protected so you cannot push your code to it directly).
3. Create python file (.py) under "players" folder with your name (lower case and underscore for spaces).
4. Write the following:

 
    import classes.api as game_api

    class <Your script name in camel case>:

    def __init__(self):
        <Your init code here>
    
    def do_turn(self, game_api: game_api.API):
        <Your code to execute each turn here>

4. commit and push your code to the remote (origin) and ask for a pull request.
5. I will check that everything is ok and confirm if so.



