from dotenv import load_dotenv

load_dotenv('secrets.env')

import discord
import os
from commands import BotCommands

bot = discord.Bot()
bot.add_cog(BotCommands(bot))

bot.run(os.getenv("BOT_TOKEN"))
