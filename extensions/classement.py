from discord.ext import commands
import discord
import datetime
from datetime import timedelta
from discord import app_commands
import typing
from discord import utils as utils


def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions
def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions

class Classement(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot

    # CLASSEMENT HEURE - JOUR - DAY - SEMAINE - MOIS - TOTAL

    @app_commands.command(description='Classement du nombre de messages')
    @app_commands.choices(choix=[
            app_commands.Choice(name="Heure", value="heure"),
            app_commands.Choice(name="Aujourd'hui", value="jour"),
            app_commands.Choice(name="Jour spécifique", value="jour_j"),
            app_commands.Choice(name="Semaine", value="semaine"),
            app_commands.Choice(name="Mois", value="mois"),
            app_commands.Choice(name="Total", value="total"),
            ])
    @app_commands.describe(choix = "Choisir le type de classement voulut", jour ="Jour spécifique uniquement pour un jour j, du type JJ/MM/AAAA")
    async def classement(self,interaction : discord.Interaction, choix : app_commands.Choice[str], jour :typing.Optional[str]):
        print(f"\033[0;34mLa commande /classement_{choix.value} a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m")           
        if is_staff(interaction.user):
            acceptable_roles = ["Bois", "Candidats", "Testeur"]
            if choix.value == 'heure':
                await interaction.response.send_message(
                    "La commande a été reconnue, veuillez patienter", ephemeral=False)
                message_count = {}
                total_messages = 0

                # Calcul de la date de début (il y a une heure)
                one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
                for channel in interaction.guild.text_channels:
                    async for message in channel.history(limit=None, after=one_hour_ago):

                        if message.author and not message.author.bot:

                            if isinstance(message.author, discord.Member):
                                # Liste des noms de rôles acceptables
                                

                                # Vérifier si l'utilisateur a au moins l'un des rôles acceptables
                                has_acceptable_role = any(role.name in acceptable_roles
                                                            for role in message.author.roles)

                                if has_acceptable_role:
                                    total_messages += 1
                                    user_id = message.author.id
                                    if user_id not in message_count:
                                        message_count[user_id] = 1
                                    else:
                                        message_count[user_id] += 1

                sorted_users = sorted(message_count.items(),
                                        key=lambda x: x[1],
                                        reverse=True)
                top_users = sorted_users[:25]
                

                embed = discord.Embed(
                    
                    color=discord.Colour(0xd14b00))

                for rank, (user_id, count) in enumerate(top_users, start=1):
                    user = interaction.guild.get_member(user_id)
                    
                    if user is None:
                        continue

                    percentage = (count / total_messages) * 100 if total_messages > 0 else 0
                    embed.add_field(name=f"{rank}. {user.display_name}",
                                    value=f"{count} messages ({percentage:.2f}%)",
                                    inline=False)
                embed.set_footer(
                    text=f"Nombre total de messages durant l'heure : {total_messages}")
                embed.set_author(name='Classement des utilisateurs les plus actifs la dernière heure',icon_url='https://i.goopics.net/xilgp9.gif')

                await interaction.channel.send(embed=embed)
            elif choix.value == 'jour':
                await interaction.response.send_message(
                    "La commande a été reconnue, veuillez patienter", ephemeral=False)
                message_count = {}
                total_messages = 0

                # Calcul de la date de début (aujourd'hui)
                today = datetime.datetime.now().date()
                start_of_day = datetime.datetime.combine(today, datetime.time.min)
                end_of_day = datetime.datetime.combine(today, datetime.time.max)

                for channel in interaction.guild.text_channels:
                    async for message in channel.history(limit=None,
                                                        after=start_of_day,
                                                        before=end_of_day):

                        if message.author and not message.author.bot:
                            if isinstance(message.author, discord.Member):
                            # Liste des noms de rôles acceptables
                            

                                # Vérifier si l'utilisateur a au moins l'un des rôles acceptables
                                has_acceptable_role = any(role.name in acceptable_roles
                                                            for role in message.author.roles)

                                if has_acceptable_role:
                                    total_messages += 1
                                    user_id = message.author.id
                                    if user_id not in message_count:
                                        message_count[user_id] = 1
                                    else:
                                        message_count[user_id] += 1

                sorted_users = sorted(message_count.items(),
                                        key=lambda x: x[1],
                                        reverse=True)
                top_users = sorted_users[:25]

                embed = discord.Embed(
                    
                    color=discord.Colour(0xd14b00))
                for rank, (user_id, count) in enumerate(top_users, start=1):
                    user = interaction.guild.get_member(user_id)

                    if user:
                        percentage = (count /
                                        total_messages) * 100 if total_messages > 0 else 0
                        embed.add_field(name=f"{rank}. {user.display_name}",
                                    value=f"{count} messages ({percentage:.2f}%)",
                                    inline=False)
                embed.set_footer(
                    text=f"Nombre total de messages aujourd'hui : {total_messages}")
                embed.set_author(name="Classement des utilisateurs les plus actifs aujourd'hui",icon_url='https://i.goopics.net/xilgp9.gif')
                await interaction.channel.send(embed=embed)
            elif choix.value == 'jour_j':
                await interaction.response.send_message(
                    "La commande a été reconnue, veuillez patienter", ephemeral=False)
                try:
                    # Analyser la date fournie dans le format jour/mois/année (par exemple, "23/08/2023")
                    date = datetime.datetime.strptime(jour, "%d/%m/%Y").date()
                except ValueError:
                    await interaction.channel.send(
                        "Format de date incorrect. Utilisez le format jour/mois/année (par exemple, 23/08/2023)."
                    )
                    return

                message_count = {}
                total_messages = 0

                start_of_day = datetime.datetime.combine(date, datetime.time.min)
                end_of_day = datetime.datetime.combine(date, datetime.time.max)

                for channel in interaction.guild.text_channels:
                    async for message in channel.history(limit=None,
                                                        after=start_of_day,
                                                        before=end_of_day):

                        if message.author and not message.author.bot:
                            if isinstance(message.author, discord.Member):
                            # Liste des noms de rôles acceptables
                            

                            # Vérifier si l'utilisateur a au moins l'un des rôles acceptables
                                has_acceptable_role = any(role.name in acceptable_roles
                                                            for role in message.author.roles)

                                if has_acceptable_role:
                                    total_messages += 1
                                    user_id = message.author.id
                                    if user_id not in message_count:
                                        message_count[user_id] = 1
                                    else:
                                        message_count[user_id] += 1

                sorted_users = sorted(message_count.items(),
                                        key=lambda x: x[1],
                                        reverse=True)
                top_users = sorted_users[:25]

                embed = discord.Embed(

                    color=discord.Colour(0xd14b00))
                total_messages = sum(count for _, count in top_users)

                for rank, (user_id, count) in enumerate(top_users, start=1):
                    user = interaction.guild.get_member(user_id)
                    if user:
                        percentage = (count /
                                        total_messages) * 100 if total_messages > 0 else 0
                        embed.add_field(name=f"{rank}. {user.display_name}",
                                    value=f"{count} messages ({percentage:.2f}%)",
                                    inline=False)
                embed.set_footer(
                    text=f"Nombre total de messages le {jour} : {total_messages}")
                embed.set_author(name=f'Classement des utilisateurs les plus actifs le {jour}',icon_url='https://i.goopics.net/xilgp9.gif')
                await interaction.channel.send(embed=embed)
            elif choix.value == 'semaine':
                await interaction.response.send_message(
                    "La commande a été reconnue, veuillez patienter", ephemeral=False)
                message_count = {}
                total_messages = 0

                # Calcul de la date de début (il y a une semaine)
                one_week_ago = datetime.datetime.now() - datetime.timedelta(weeks=1)

                for channel in interaction.guild.text_channels:
                    async for message in channel.history(limit=None, after=one_week_ago):

                        if message.author and not message.author.bot:
                            if isinstance(message.author, discord.Member):
                            # Liste des noms de rôles acceptables
                            

                            # Vérifier si l'utilisateur a au moins l'un des rôles acceptables
                                has_acceptable_role = any(role.name in acceptable_roles
                                                            for role in message.author.roles)

                                if has_acceptable_role:
                                    total_messages += 1
                                    user_id = message.author.id
                                    if user_id not in message_count:
                                        message_count[user_id] = 1
                                    else:
                                        message_count[user_id] += 1

                sorted_users = sorted(message_count.items(),
                                        key=lambda x: x[1],
                                        reverse=True)
                top_users = sorted_users[:25]

                embed = discord.Embed(
                    
                    color=discord.Colour(0xd14b00))
                for rank, (user_id, count) in enumerate(top_users, start=1):
                    user = interaction.guild.get_member(user_id)
                    if user:
                        percentage = (count /
                                        total_messages) * 100 if total_messages > 0 else 0
                        embed.add_field(name=f"{rank}. {user.display_name}",
                                    value=f"{count} messages ({percentage:.2f}%)",
                                    inline=False)
                embed.set_footer(
                    text=f"Nombre total de messages de la semaine : {total_messages}")
                embed.set_author(name='Classement des utilisateurs les plus actifs cette semaine',icon_url='https://i.goopics.net/xilgp9.gif')
                await interaction.channel.send(embed=embed)
            elif choix.value == 'mois':
                await interaction.response.send_message(
                    "La commande a été reconnue, veuillez patienter", ephemeral=False)
                message_count = {}
                total_messages = 0  # Initialisez la variable total_messages

                # Calcul de la date de début (il y a un mois)
                one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)

                for channel in interaction.guild.text_channels:
                    async for message in channel.history(limit=None, after=one_month_ago):
                        if message.author and not message.author.bot:
                            if isinstance(message.author, discord.Member):
                            # Liste des noms de rôles acceptables
                            

                                # Vérifier si l'utilisateur a au moins l'un des rôles acceptables
                                has_acceptable_role = any(role.name in acceptable_roles
                                                            for role in message.author.roles)

                                if has_acceptable_role:
                                    total_messages += 1
                                    user_id = message.author.id
                                    if user_id not in message_count:
                                        message_count[user_id] = 1
                                    else:
                                        message_count[user_id] += 1

                sorted_users = sorted(message_count.items(),
                                        key=lambda x: x[1],
                                        reverse=True)
                top_users = sorted_users[:25]

                embed = discord.Embed(
                    
                    color=discord.Colour(0xd14b00))
                for rank, (user_id, count) in enumerate(top_users, start=1):
                    user = interaction.guild.get_member(user_id)
                    if user:
                        percentage = (count /
                                        total_messages) * 100 if total_messages > 0 else 0
                        embed.add_field(name=f"{rank}. {user.display_name}",
                                    value=f"{count} messages ({percentage:.2f}%)",
                                    inline=False)
                embed.set_footer(
                    text=f"Nombre total de messages du mois : {total_messages}")
                embed.set_author(name='Classement des utilisateurs les plus actifs ce mois',icon_url='https://i.goopics.net/xilgp9.gif')
                await interaction.channel.send(embed=embed)
            elif choix.value == 'total':
                await interaction.response.send_message(
                    "La commande a été reconnue, veuillez patienter", ephemeral=False)
                message_count = {}
                total_messages = 0

                for channel in interaction.guild.text_channels:
                    async for message in channel.history(limit=None):

                        if message.author and not message.author.bot:
                            if isinstance(message.author, discord.Member):
                            # Liste des noms de rôles acceptables
                            

                                # Vérifier si l'utilisateur a au moins l'un des rôles acceptables
                                has_acceptable_role = any(role.name in acceptable_roles
                                                            for role in message.author.roles)

                                if has_acceptable_role:
                                    total_messages += 1
                                    user_id = message.author.id
                                    if user_id not in message_count:
                                        message_count[user_id] = 1
                                    else:
                                        message_count[user_id] += 1

                sorted_users = sorted(message_count.items(),
                                        key=lambda x: x[1],
                                        reverse=True)
                top_users = sorted_users[:25]
                

                embed = discord.Embed(
                    
                    color=discord.Colour(0xd14b00))

                for rank, (user_id, count) in enumerate(top_users, start=1):
                    user = interaction.guild.get_member(user_id)

                    if user:
                        percentage = (count /
                                        total_messages) * 100 if total_messages > 0 else 0
                        embed.add_field(name=f"{rank}. {user.display_name}",
                                    value=f"{count} messages ({percentage:.2f}%)",
                                    inline=False)
                embed.set_footer(text=f"Nombre total de messages : {total_messages}")
                embed.set_author(name='Classement global des utilisateurs les plus actifs',icon_url='https://i.goopics.net/xilgp9.gif')

                await interaction.channel.send(embed=embed)
            else:
                await interaction.response.send_message("Il y a un problème", ephemeral=True)
        else:
            await interaction.response.send_message(
                "Vous devez être modérateur ou administrateur pour utiliser cette commande.",
                ephemeral=True)
        


async def setup(bot):
  await bot.add_cog(Classement(bot))

  