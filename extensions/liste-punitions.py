from discord.ext import commands
import discord
import datetime
from datetime import timedelta
from discord import app_commands
import extensions.config as config
from discord import utils as utils

from pymongo.mongo_client import MongoClient


def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions

def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions



mongo_uri = config.MONGODB_URI


client = MongoClient(mongo_uri)
db = client.laylosupport

try:
    client.admin.command('ping')
except Exception as e:
    print("error")


class Punitions(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot

    # SANCTION LISTER

    @app_commands.command(description="Liste toutes les sanctions d'un utilisateur")
    @app_commands.describe(membre="Membre dont vous souhaitez obtenir la liste de sanctions")
    async def sanction(self, interaction:discord.Interaction, membre : discord.Member):
        cmd_use=f'\033[0;34mLa commande /sanction a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)
        if is_staff(interaction.user):
            id_sanc = db.id_sanction.find()
            kick = 0
            warn = 0
            mute = 0
            ban = 0
            total = ""
            user_sanctionnee = False
            for id in id_sanc:
                id_bdd_sanction = id["id"]
                if id_bdd_sanction == membre.id:
                    user_sanctionnee = True
            if user_sanctionnee == True:
                sanction = db.moderation.find()
                embed = discord.Embed(color=0xd14b00)
                embed.set_author(name=f'Historique de {membre.global_name} (@{membre.name})',icon_url='https://i.goopics.net/xilgp9.gif')
                maintenant = datetime.datetime.now()
                date = maintenant.strftime('%d/%m/%Y %H:%M')
                embed.set_footer(text=f"Communauté Laylo • {date}")
                for sanctions in sanction:
                    id_bdd = sanctions["Id"]
                    if id_bdd == membre.id:
                        s = str(sanctions["Sanction"])
                        v = sanctions["value"]
                        j = sanctions["Jour"]
                        r = sanctions["Raison"]
                        m = sanctions["Usermod"]
                        m2 = sanctions["Modérateur"]
                        if "Durée" in sanctions:
                            d =  sanctions["Durée"]
                        else:
                            d = "Aucune durée définie"  
                        if v == "kick":
                            kick+=1
                        elif v == "mute":
                            mute+=1
                        elif v == "warn":
                            warn+=1
                        elif v == "ban":
                            ban +=1
                        embed.add_field(name=f"\n{s} - {j} \n", value=f"> **Durée :** {d} \n> **Modérateur : ** {m2} ``(@{m})`` \n> **Raison :** {r}", inline=False)
                if warn !=0:
                        total += f"・{warn} warn(s) "
                if mute !=0:
                        total += f"・{mute} mute(s)"
                if kick !=0:
                        total+= f"・{kick} kick(s)"
                if ban != 0:
                        total+= f"・{ban} ban(s)"
                
                embed.description = f"🔎 **{total}**"
                await interaction.response.send_message(embed=embed)        
            else:
                await interaction.response.send_message(f"{membre.mention} n'a reçu aucune sanction !", ephemeral=True)
                
        else:
            await interaction.response.send_message(
                "Vous devez être modérateur pour utiliser cette commande !",
                ephemeral=True)



async def setup(bot):
  await bot.add_cog(Punitions(bot))

  