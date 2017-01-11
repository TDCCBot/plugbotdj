import discord, os, random, sys, time
from discord.ext import commands
#I don't know which imports you need for a minimalist setup, but these should be good enough
#Just copied from mine and cut it down a lot
#Example, you may not need asyncio. uwu
#Note: I will test on 3.4, using 3.4 syntax then convert to 3.5. I'll my best to do a full conversion.

try:
	import asyncio
except:
	print("Can't import asyncio. Might not matter tho.")

try:
	import sqlite3
except:
	try:
		import pip
		pip.main(['install', "sqlite3"])
		import sqlite3
	except:
		print("Print can't import pip / install sqlite3. This is more of an issue uwu")


client = discord.Client()
bot = commands.Bot(command_prefix='$$', description="Anitwitter Discord Bot")

#Global Vars

sql_connection = sqlite3.connect("database.db")
sql_cursor = sql_connection.cursor()

#Commands
@bot.command(pass_context=True)
async def getCount(ctx):
	try:
		userid = ctx.message.author.id
		dbInput = (userid, )
		sql_cursor.execute("SELECT count FROM messages WHERE userid=?", dbInput)
		dbOutput = sql_cursor.fetchone()[0]
		await bot.send_message(ctx.message.channel, "You have %s in your account." %str(int(dbOutput / 5 )* 10))#This is the calculation innit fam.
	except TypeError:
		await bot.send_message(ctx.message.channel, "You have 0 messages. You might need to talk more.")
	except Exception as e:
		await bot.send_message(ctx.message.channel, str(e))

#Events
@bot.event
async def on_message(message):
	#########
	# Begin Count#
	#########
	userid = message.author.id
	username = str(message.author)
	currentMessages = 0
	dbInput = (userid,)
	sql_cursor.execute("SELECT EXISTS(SELECT 1 FROM messages WHERE userid=? LIMIT 1);", dbInput)
	dbOutput = sql_cursor.fetchone()[0]
	if dbOutput == 1:
		#update an account
		dbInput = (userid,)
		sql_cursor.execute("SELECT count FROM messages WHERE userid=? LIMIT 1", dbInput)
		currentMessages = int(sql_cursor.fetchone()[0])
		dbInput = (currentMessages + 1, userid)
		sql_cursor.execute("UPDATE messages SET count = ? WHERE userid=?", dbInput)
	elif dbOutput == 0:
		#create new account
		dbInput = (userid, username, 1)
		sql_cursor.execute("INSERT INTO messages VALUES(?, ?, ?)", dbInput)
	sql_connection.commit()
	########
	#End Count#
	########

	#This is how I overwrite the !help command
	if message.content.startswith("$$help"): #Change depending on prefix obviously famalam
		helpMessage = "**Commands:**\n\t$$getCount - Get Points\n\t$$help - Shows This Message\n**Info:**\n\tYou get 10 points for every 5 messages you send."
		embed = discord.Embed(description=helpMessage, colour=0x00FF00, url="http://twitter.com/hbnothp")
		if bot.user.avatar_url != None:
			embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
		else:
			embed.set_author(name=bot.user.name, icon_url=bot.user.default_avatar_url)
		embed.set_footer(text="Bot developed by @HBnotHP")
		await bot.send_message(message.channel, embed=embed) 
	else:
		await bot.process_commands(message) # Run commands


#Final Initialisation
token = "MjY4NzU5MDM2OTk0NzgxMTg0.C1fc8Q.bQci9u4X2RbsvaEvKR7q3h7tJPI" #Enter your bot token here, or use a different method. 
print("Starting!")
bot.run(token)