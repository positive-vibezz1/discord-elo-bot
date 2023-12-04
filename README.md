# discord-elo-bot
a bot that can take teams and sort them by MMR using discord.py

##the bot is **half baked**, but it does work to create teams and give them mmr, but the rest of the bot is broken

the commands are
- create_team: which propts users to give the team a name, make a person a captain, and to add players 
- submit_scores: which prompts the users to enter the team names and team scores, and gives them the respecitve mmr 
- register_sub: this is supposed to rigster a player into the database as a sub and give the sub role, idk if it works because it doesnt give the role, but it look like its adding users into the player base just fine 

to run the bot download the zip, create a bot here [discord developer portal](https://discord.com/developers/applications/) and create your bot.
then open the main file which is vrml_elo_bot, and replace 
***bot.run('BOT TOKEN')***
with your bots token which can be found here
---
![Screenshot (155)](https://github.com/positive-vibezz1/discord-elo-bot/assets/134086715/7f3720f1-8c0a-4c05-871c-93de17ffae0f)
---

then replace all the ***ranking_and_teams_channel = "replace with your desgnated channel"*** with the channel you want the bot to see the commands and replay to them.
there should be three variables you have to replace
-vrml_elo_bot; which is at line 35 
-create_team; which is at line 12 
ranking_class; which is at line 17 
