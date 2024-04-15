import discord
from discord.ext import commands
from discord import utils as utils
import os

from extensions.ticket import ticket_launcher, confirm, main, confirmation2
from extensions.drop import bouton_drop
import extensions.config as config



async def load():
    for filename in os.listdir('extensions'):
        if filename.endswith('.py'):
            if filename.startswith('config'):
                pass
            else:
                await bot.load_extension(f"extensions.{filename[:-3]}")


class Mybot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!!!!!", intents=discord.Intents.all())
    async def setup_hook(self):
             await load()
             await self.tree.sync()
             self.add_view(ticket_launcher())
             self.add_view(confirm())
             self.add_view(main())
             self.add_view(confirmation2())
             self.add_view(bouton_drop())
             
bot = Mybot()
bot.remove_command('help')



@bot.event
async def on_ready():
  print(
      f'\033[1;4;92mLE BOT EST PRET, LA SESSION EST OUVERTE DEPUIS LE {bot.user.name}\033[0m'
  )
  print(f'\033[1;4;96mCOGS SYNCRONISES !\033[0m')


  guild = bot.get_guild(
      703325860585013249)  # Lance la tâche périodique
  activity = discord.Activity(
        name=f"{len(guild.members)} membres chez Laylo",
        type=discord.ActivityType.watching,

    )
  await bot.change_presence(activity=activity)
  
  

bot.run(config.TOKEN)