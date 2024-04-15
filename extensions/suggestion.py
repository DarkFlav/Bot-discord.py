from discord.ext import commands
import discord
import datetime
from datetime import timedelta
from discord import app_commands
import extensions.config as config
from discord import utils as utils


def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions
def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions

class Suggestion(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot

    # SUGGESTION CREATE
        
    @app_commands.command(description="Créer une suggestion")
    @app_commands.describe(titre ="Titre de votre suggestion",suggestion ="Contenu de la suggestion")
    async def suggestion(self, interaction : discord.Interaction, titre : str, suggestion: str):
        print(f'\033[0;34mLa commande /suggestion a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        embed = discord.Embed(color=0xd14b00, title=titre, description=suggestion)
        embed.set_author(name=interaction.user.display_name,icon_url=interaction.user.display_avatar.url)
        maintenant = datetime.datetime.now()
        date = maintenant.strftime('%d/%m/%Y %H:%M')
        embed.set_footer(text=f"Communauté Laylo • {date}", icon_url='https://i.goopics.net/xilgp9.gif')
        await interaction.response.send_message('La suggestion a bien été postée !', ephemeral=True)
        channel_suggest = discord.utils.get(interaction.guild.channels, id=config.suggest_channel_id)
        msg = await channel_suggest.send(embed=embed)
        
        await msg.add_reaction("✅")
        await msg.add_reaction("➖")
        await msg.add_reaction("❌")
        await msg.create_thread(name=f"Suggestion de {interaction.user.name}",
                                            slowmode_delay=10) 



    #SUGGESTMOD ACCEPTER ET REFUSER (CHOICES)

    @app_commands.command(description='Accepter ou refuser une suggestion')
    @app_commands.choices(choix=[
            app_commands.Choice(name="Accepter", value="accepter"),
            app_commands.Choice(name="Refuser", value="refuser"),
            ])
    @app_commands.describe(choix = "Accepter ou refuser", raison ="Raison de la validation ou du refus", id ="Identifiant de la suggestion")
    async def suggestmod(self, interaction : discord.Interaction, choix : app_commands.Choice[str], raison : str, id : str):
        cmd_use=f'\033[0;34mLa commande /suggestmod a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)
        if is_staff(interaction.user):
            choix = str(choix)
            if choix == "Choice(name='Accepter', value='accepter')":
                id = int(id)
                suggest_channel_id = 1046820259170091099
                suggest_channel = interaction.guild.get_channel(suggest_channel_id)
                try:
                    message = await suggest_channel.fetch_message(id)
                    if message.embeds:
                        # Récupérer le premier embed
                        embed = message.embeds[0]
                        nouvel_embed = discord.Embed(
                            title=embed.title,
                            description=embed.description,
                            url=embed.url,
                            color=0x40f000,
                            
                        )
                        nouvel_embed.set_footer(text=embed.footer.text, icon_url=embed.footer.icon_url)
                        nouvel_embed.set_author(name=embed.author.name +f"  - ✅ Suggestion validée par {interaction.user.display_name}", icon_url=embed.author.icon_url)
                        nouvel_embed.add_field(name="__Raison de l'acceptation :__",value=f"\n > {raison}")
                        await message.edit(embed=nouvel_embed)
                        await interaction.response.send_message("La suggestion a bien été acceptée !", ephemeral=True)
                    else:
                        await interaction.response.send_message("Ce n'est pas une suggestion !", ephemeral=True)
                except:
                    await interaction.response.send_message("Le message de la suggestion n'a pas été trouver", ephemeral=True)
            elif choix =="Choice(name='Refuser', value='refuser')":
                id = int(id)
                suggest_channel_id = 1046820259170091099
                suggest_channel = interaction.guild.get_channel(suggest_channel_id)
                try:
                    message = await suggest_channel.fetch_message(id)
                    if message.embeds:
                        # Récupérer le premier embed
                        embed = message.embeds[0]
                        nouvel_embed = discord.Embed(
                            title=embed.title,
                            description=embed.description,
                            url=embed.url,
                            color=0xF00000,
                            
                        )
                        nouvel_embed.set_footer(text=embed.footer.text, icon_url=embed.footer.icon_url)
                        nouvel_embed.set_author(name=embed.author.name +f"  - ❌ Suggestion refusée par {interaction.user.display_name}", icon_url=embed.author.icon_url)
                        nouvel_embed.add_field(name="__Raison du refus :__",value=f"\n > {raison}")
                        await message.edit(embed=nouvel_embed)
                        await interaction.response.send_message("La suggestion a bien été refusée !", ephemeral=True)
                    else:
                        await interaction.response.send_message("Ce n'est pas une suggestion !", ephemeral=True)
                except:
                    await interaction.response.send_message("Le message de la suggestion n'a pas été trouver", ephemeral=True)
            else:
                await interaction.response.send_message("Il y a eu un problème !", ephemeral=True)
        else:
            await interaction.response.send_message("Vous devez être modérateur ou administrateur pour utiliser cette commande.", ephemeral=True)



async def setup(bot):
  await bot.add_cog(Suggestion(bot))

  