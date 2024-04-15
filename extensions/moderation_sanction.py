from discord.ext import commands
import discord
import datetime
from datetime import timedelta
from discord import app_commands
import extensions.config as config
from discord import utils as utils
from humanfriendly import parse_timespan

from pymongo.mongo_client import MongoClient

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



mongo_uri = config.MONGODB_URI


client = MongoClient(mongo_uri)
db = client.laylosupport

try:
    client.admin.command('ping')
    print(
      f'\033[1;4;95mCONNECTE A MONGODB !\033[0m'
  )
except Exception as e:
    print("error")


class ModerationSanction(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot



    # MUTE QQN 

    @app_commands.command(description="Réduire un membre au silence")
    @app_commands.describe(membre="Membre à réduire au silence",temps="Temps de la réduction au silence (ex : 1d, 15min..)",raison="Raison de la réduction au silence")
    async def mute(self, interaction:discord.Interaction, membre:discord.Member, temps : str, raison : str):
        cmd_use=f'\033[0;34mLa commande /mute a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)
        if is_staff_test(interaction.user):
            if is_staff(membre) or is_staff_test(membre):
                await interaction.response.send_message(f"Vous ne pouvez pas mute {membre.mention}, car il a des permissions de modération", ephemeral=True)
            else:
                try :
                    temps_reel = parse_timespan(temps)
                except:
                    await interaction.response.send_message("La durée n'est pas valide", ephemeral=True)
                else:
                    if not membre.is_timed_out():
                        try:
                            await membre.timeout(utils.utcnow()+timedelta(seconds=temps_reel))
                            embed = discord.Embed(
                                color=discord.Colour(0xd14b00),
                                description=f"Le membre **{membre}**``(@{membre.name})`` a été **réduit au silence **{temps} \n > Raison : {raison}")
                            
                            embed.set_author(name='Sanction',icon_url='https://i.goopics.net/xilgp9.gif')
                            await interaction.response.send_message(embed=embed)

                            embed2 = discord.Embed(
                                color=discord.Colour(0xd14b00),
                                description=f"Vous avez été **réduit au silence **{temps} sur le serveur **{interaction.guild.name}** \n > Raison : {raison}\n     \n **Modérateur** : {interaction.user.display_name}")
                            embed2.set_author(name='Sanction',icon_url='https://i.goopics.net/xilgp9.gif')
                            await membre.send(embed=embed2)


                            mute = {
                                "Utilisateur" : membre.display_name,
                                "Id" : membre.id,
                                "Sanction" : "Réduction au silence temporaire",
                                "Durée" : str(temps),
                                "Raison" : str(raison),
                                "Modérateur" : interaction.user.display_name,
                                "Usermod" : interaction.user.name,
                                "Jour" : timestamp(),
                                "value" : "mute"
                            }
                            
                            db.moderation.insert_one(mute)
                            id_sanc = db.id_sanction.find()
                            a=0
                            for id in id_sanc:
                                    id_bdd = id["id"]
                                    if id_bdd == membre.id:
                                        a=1
                            if a!=1:
                                    id_sanc_add = {
                                'id': membre.id,
                                }
                                    db.id_sanction.insert_one(id_sanc_add)

                        except:
                            await interaction.response.send_message(f"Vous ne pouvez pas rendre muet {membre.mention} !", ephemeral=True)
                    else:
                        embed=discord.Embed(color=discord.Colour(0xd14b00),
                            description=f"{membre.mention} est déja réduit au silence !")
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                
        else:
            await interaction.response.send_message("Vous devez être modérateur pour effectuer cette commande", ephemeral=True)
        
    # DEMUTE QQN

    @app_commands.command(description="Retirer la réduction d'un membre au silence")
    @app_commands.describe(membre ="Membre à qui vous voulez retirer le mute")
    async def demute(self, interaction:discord.Interaction, membre:discord.Member):
        cmd_use=f'\033[0;34mLa commande /demute a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)
        if is_staff_test(interaction.user):
            if not membre.is_timed_out():
                embed=discord.Embed(color=discord.Colour(0xd14b00),
                            description=f"{membre.mention} n'est pas réduit au silence !")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                try:
                    await membre.timeout(None)
                except:
                    embed=discord.Embed(color=discord.Colour(0xd14b00),
                            description=f"{membre.mention} n'a pas pu être unmute!")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    embed=discord.Embed(color=discord.Colour(0xd14b00),
                            description=f"Le membre **{membre}**``(@{membre.name})`` a pu retrouver la parole !!")
                    embed.set_author(name='Sanction',icon_url='https://i.goopics.net/xilgp9.gif')
                    await interaction.response.send_message(embed=embed)
                    embed2 = discord.Embed(
                        color=discord.Colour(0xd14b00),
                            description=f"Vous n'êtes plus** réduit au silence** sur le serveur **{interaction.guild.name}**\n\n **Modérateur** : {interaction.user.display_name}")
                    embed2.set_author(name='Sanction',icon_url='https://i.goopics.net/xilgp9.gif')
                    await membre.send(embed=embed2)
        else:
            await interaction.response.send_message(
                "Vous devez être modérateur ou administrateur pour utiliser cette commande.",
                ephemeral=True)

    # WARN QQN

    @app_commands.command(description="Avertir une personne")
    @app_commands.describe(membre='Membre à avertir',raison='Raison de la réduction au silence')
    async def warn(self, interaction: discord.Interaction, membre:discord.Member, raison : str):
        cmd_use=f'\033[0;34mLa commande /warn a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)
        if is_staff_test(interaction.user):
            if is_staff(membre) or is_staff_test(membre):
                await interaction.response.send_message(f"Vous ne pouvez pas warn {membre.mention}, car il a des permissions de modération", ephemeral=True)
            else:
                embed = discord.Embed(
                            color=discord.Colour(0xd14b00),
                            description=f"Le membre **{membre}**``(@{membre.name})`` a été **avertit **\n > Raison : {raison}")
                        
                embed.set_author(name='Sanction',icon_url='https://i.goopics.net/xilgp9.gif')
                await interaction.response.send_message(embed=embed)

                embed2 = discord.Embed(
                            color=discord.Colour(0xd14b00),
                            description=f"Vous avez été **avertit** sur le serveur **{interaction.guild.name}** \n > Raison : {raison}\n     \n **Modérateur** : {interaction.user.display_name}")
                embed2.set_author(name='Sanction',icon_url='https://i.goopics.net/xilgp9.gif')
                await membre.send(embed=embed2)


                warn = {
                            "Utilisateur" : membre.display_name,
                            "Id" : membre.id,
                            "Sanction" : "Avertissement",
                            "Raison" : str(raison),
                            "Modérateur" : interaction.user.display_name,
                            "Usermod": interaction.user.name,
                            "Jour" : timestamp(),
                            "value" : "warn",
                            
                        }
                db.moderation.insert_one(warn)
                id_sanc = db.id_sanction.find()
                a=0
                for id in id_sanc:
                        id_bdd = id["id"]
                        if id_bdd == membre.id:
                            a=1
                if a!=1:
                        id_sanc_add = {
                    'id': membre.id,
                    }
                        db.id_sanction.insert_one(id_sanc_add)

        else:
            await interaction.response.send_message(
                "Vous devez être modérateur ou administrateur pour utiliser cette commande.",
                ephemeral=True)

    # KICK QQN
        
    @app_commands.command(description="Expulser quelqu'un du serveur")
    @app_commands.describe(membre='Membre à expulser',raison="Raison de l'expulsion")
    async def kick(self, interaction: discord.Interaction, membre:discord.Member, raison : str):
        cmd_use=f'\033[0;34mLa commande /kick a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)
        if is_staff(interaction.user):
            if is_staff(membre) or is_staff_test(membre):
                await interaction.response.send_message(f"Vous ne pouvez pas kick {membre.mention}, car il a des permissions de modération", ephemeral=True)
            else:
                try:


                        embed2 = discord.Embed(
                            color=discord.Colour(0xd14b00),
                            description=f"Vous avez été **expulsé** sur le serveur **{interaction.guild.name}** \n > Raison : {raison}\n     \n **Modérateur** : {interaction.user.display_name}")
                        embed2.set_author(name='Sanction',icon_url='https://i.goopics.net/xilgp9.gif')
                        await membre.send(embed=embed2)
                        await membre.kick()

                        embed = discord.Embed(
                            color=discord.Colour(0xd14b00),
                            description=f"Le membre **{membre}**``(@{membre.name})`` a été **expulsé du serveur ! \n > Raison : {raison}")
                        
                        embed.set_author(name='Sanction',icon_url='https://i.goopics.net/xilgp9.gif')
                        await interaction.response.send_message(embed=embed)

                        


                        kick = {
                            "Utilisateur" : membre.display_name,
                            "Usermod":interaction.user.name,
                            "Id" : membre.id,
                            "Sanction" : "Expulsion du serveur",
                            "Raison" : str(raison),
                            "Modérateur" : interaction.user.display_name,
                            "Jour" : timestamp(),
                            "value":"kick",
                        }
                        
                        db.moderation.insert_one(kick)

                        id_sanc = db.id_sanction.find()
                        a=0
                        for id in id_sanc:
                            id_bdd = id["id"]
                            if id_bdd == membre.id:
                                a=1
                        if a!=1:
                            id_sanc_add = {
                        'id': membre.id,
                    }
                            db.id_sanction.insert_one(id_sanc_add)

                        
                except:
                        await interaction.response.send_message(f"Vous ne pouvez pas expulser {membre.mention} !", ephemeral=True)
        else:
            await interaction.response.send_message(
                "Vous devez être modérateur ou administrateur pour utiliser cette commande.",
                ephemeral=True)

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
  await bot.add_cog(ModerationSanction(bot))

  