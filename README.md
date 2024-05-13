# discord-elo-bot
a bot that can take teams and sort them by MMR using discord.py

## the bot is **half baked**, but it does work to create teams and give them mmr, but the rest of the bot is broken

the commands are
- create_team: which prompts users to give the team a name, make a person a captain, and to add players 
- submit_scores: which prompts the users to enter the team names and team scores, and gives them the respecitve mmr 
- register_sub: this is supposed to register a player into the database as a sub and give the sub role, idk if it works because it doesnt give the role, but it look like its adding users into the player base just fine.

to run the bot download the files, and send them all to one folder, its important you do this, create a bot here [discord developer portal](https://discord.com/developers/applications/) and create your bot.
then open the main file which is vrml_elo_bot, and replace 
***bot.run('BOT TOKEN')***
with your bots token which can be found here

![Screenshot (155)](https://github.com/positive-vibezz1/discord-elo-bot/assets/134086715/7f3720f1-8c0a-4c05-871c-93de17ffae0f)
---

then replace all the ***ranking_and_teams_channel = "replace with your desgnated channel"***
- vrml_elo_bot at line 35
- ranking_class at line 17
- creat_team at line 12
with the channel you want the bot to see the commands and reply to them(there may be more; if so when debugging the code it will throw an error to where the ***ranking_and_teams_channel = "replace with your desgnated channel"*** is located, i think)
there should be three variables you have to replace
- vrml_elo_bot; which is at line 35 
- create_team; which is at line 12 
- ranking_class; which is at line 17 

---
## About the `register_sub and substitute files` 
they shouldnt be to hard to fix for the ppl that know how, the only problem is im a novice coder, and this bot just kept getting bigger and bigger, and more stuff just kept being needed, ability to create substitutes, add/remove players/ ability for players to leave teams, ability to check teams mmr, ability to check substitutes mmr, check registered teams in the data basa, check players registred to teams in the database, and check the subs registered to the databasa, the list can go on forever, and i dont rlly understand what im doing anymore, so im calling it quite, maybe i shall come back to this bot one day when im a more expereienced programmer and fix everything, and refactor the code
