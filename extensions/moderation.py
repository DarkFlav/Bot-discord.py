from discord.ext import commands
import discord
import datetime
from datetime import timedelta
from discord import app_commands
from discord import utils as utils
import typing

def timestamp():
        # Obtenir l'heure actuelle avec datetime.now()
        now = datetime.datetime.now()

        # Convertir l'heure actuelle en timestamp UNIX
        timestamp_unix = int(now.timestamp())

        # Envoyer le résultat
        return f"<t:{timestamp_unix}:F>"

def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions

def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions






class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot


        
        


    # COMMANDE /CLEAR (NOMBRE)

    @app_commands.command(description="Supprimer un certain nombre de message")
    @app_commands.describe(nombre="Nombre de messages à supprimer",utilisateur="Utilisateur dont vous voulez supprimer les messages")
    async def clear(self, interaction: discord.Interaction,
                    nombre: app_commands.Range[int, 1,99],
                    utilisateur: typing.Optional[discord.User] = None):
        print(f"\033[0;34mLa commande /clear a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m")         
        if is_staff(interaction.user):
            messages = []
            async for message in interaction.channel.history(
                limit=nombre + 1):  # +1 pour inclure la commande
                if utilisateur is None or message.author.id == utilisateur.id:
                    messages.append(message)
                    message.author.avatar.url

            await interaction.response.send_message(
                f"{nombre} messages ont été supprimés.", ephemeral=True)
            await interaction.channel.delete_messages(messages)

        else:
            await interaction.response.send_message(
                "Vous devez être modérateur pour utiliser cette commande.",
                ephemeral=True)
     
    #SLOW CHANGE

    @app_commands.command(description="Changer le slowmod")
    @app_commands.describe(temps="Temps à mettre en seconde")
    async def slow(self, interaction: discord.Interaction, temps: app_commands.Range[int, 0,21600]):
        print(f"\033[0;34mLa commande /slow a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m") 
        if is_staff(interaction.user):
            await interaction.channel.edit(slowmode_delay=temps)
            await interaction.response.send_message(
                f"Le mode lent a été mis à {temps} secondes", ephemeral=True)
        else:
            await interaction.response.send_message(
                "Vous devez être modérateur ou administrateur pour utiliser cette commande.",
                ephemeral=True)


    # CHANGER LE PSEUDO

    @app_commands.command(description="Changer le pseudo d'une personne")
    @app_commands.describe(pseudo="Pseudo que vous souhaitez mettre à la personne",membre="Membre à qui vous voulez changer le pseudo")
    async def nick(self,interaction: discord.Interaction, membre: discord.Member, pseudo:str):
        cmd_use=f'\033[0;34mLa commande /nick a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)
        if is_staff(interaction.user):
            if membre:
                ancien_pseudo = membre.display_name
                try :
                    await membre.edit(nick=pseudo)
                    await interaction.response.send_message(f"Le pseudo de {ancien_pseudo} a bien été modifié en {pseudo}", ephemeral=False)
                except:
                    await interaction.response.send_message(f"Le pseudo de {ancien_pseudo} n'a pas pu être modifié", ephemeral=True)
            else:
                ancien_pseudo =interaction.user.display_name
                try:
                    await interaction.user.edit(nick=pseudo)
                    await interaction.response.send_message(f"Le pseudo de {ancien_pseudo} a bien été modifié en {pseudo}", ephemeral=False)

                except:
                    await interaction.response.send_message(f"Le pseudo de {ancien_pseudo} n'a pas pu être modifié", ephemeral=True)
        else:
            await interaction.response.send_message(
                "Vous devez être modérateur ou administrateur pour utiliser cette commande.",
                ephemeral=True)

async def setup(bot):
  await bot.add_cog(Moderation(bot))

  