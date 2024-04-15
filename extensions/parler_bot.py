from discord.ext import commands
import discord
import typing
from discord import app_commands
from discord import utils as utils



def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions

def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions




class Parler(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot


    # SAY

    @app_commands.command(description="Envoyer un message")
    @app_commands.describe(texte='Le texte à faire dire au bot', modifier="Lien vers le message à modifier", nombre="Nombre de fois que le message sera répété")
    async def say(self,interaction: discord.Interaction,
                texte: str,
                modifier: str = None,
                nombre: int = None):
        print(f"\033[0;34mLa commande /say a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id}) \n Il a dis {texte}.\033[0m")
        if is_staff(interaction.user):
            # Remplace "/n" par "\n" dans le texte
            texte = texte.replace("/n", "\n")

            if modifier:
            # Si un lien de message est fourni, essayez de le récupérer
                try:
                    # Divise le lien pour obtenir l'ID du message
                    message_id = int(modifier.split("/")[-1])
                    # Récupère le message
                    message_to_edit = await interaction.channel.fetch_message(message_id)
                    # Modifie le message
                    await message_to_edit.edit(content=texte)
                    await interaction.response.send_message(
                        "Le message a bien été modifié !", ephemeral=True)
                except (ValueError, discord.NotFound):
                    await interaction.response.send_message(
                        "Le lien du message n'est pas valide ou le message n'a pas été trouvé.",
                        ephemeral=True)
            else:
                if nombre:
                    await interaction.response.send_message("Le message a bien été envoyé !",
                                                            ephemeral=True)
                    for _ in range (nombre):
                    

                        await interaction.channel.send(texte)
                    
                else:
                    await interaction.response.send_message("Le message a bien été envoyé !",
                                                            ephemeral=True)
                    await interaction.channel.send(texte)
                

            
        else:
            await interaction.response.send_message(
                "Vous devez être modérateur pour utiliser cette commande !",
                ephemeral=True)


    # SAY_EMBED

    @app_commands.command(description="Envoyer un message sous forme d'embed")
    @app_commands.describe(description="La description de l'embed", titre="Le titre de l'embed", modifier="Lien vers le message à modifier",
                        nombre="Nombre de fois que le message sera répété")
    async def say_embed(self,interaction: discord.Interaction,
                        description: str,
                        titre: str = None,
                        modifier: str = None,
                        nombre: int = None):
        cmd_use=f'\033[0;34mLa commande /say_embed a été utilisée dans {interaction.channel.name} pour dire {description} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)

        if is_staff(interaction.user):
            # Remplace "/n" par "\n" dans la description
            description = description.replace("/n", "\n")

            embed = discord.Embed(description=description, color=0xd14b00, title=titre)

            if modifier:
                try:
                    message_id = int(modifier.split("/")[-1])
                    message_to_edit = await interaction.channel.fetch_message(message_id)
                    # Modifie le message avec l'embed
                    await message_to_edit.edit(embed=embed)
                    await interaction.response.send_message(
                        "Le message a bien été modifié !", ephemeral=True)
                except (ValueError, discord.NotFound):
                    await interaction.response.send_message(
                        "Le lien du message n'est pas valide ou le message n'a pas été trouvé.",
                        ephemeral=True)
            else:
                if nombre:

                    await interaction.response.send_message("Le message a bien été envoyé !",
                                                            ephemeral=True)
                    for _ in range (nombre):

                        await interaction.channel.send(embed=embed)
                else:
                    await interaction.response.send_message("Le message a bien été envoyé !",
                                                            ephemeral=True)
                    await interaction.channel.send(embed=embed)
        else:
            await interaction.response.send_message(
                "Vous devez être modérateur pour utiliser cette commande.",
                ephemeral=True)

       #BOOST

    @app_commands.command(description="Faire une annonce de boost ")
    @app_commands.describe(membre = "Membre qui a boost le serveur", nombre="Nombre de boost")
    async def boost(self,interaction : discord.Interaction, membre : discord.Member, nombre : typing.Optional[int]):
        cmd_use=f'\033[0;34mLa commande /boost a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)
        if is_staff(interaction.user):
            if nombre:
                embed = discord.Embed(color = 0xd14b00, description=f"Merci à **{membre.display_name}** pour avoir **boost** le serveur **{nombre} fois** <a:event:1150870049222054069> <a:event:1150870049222054069>")
                await interaction.response.send_message("Le message de boost a été posté !", ephemeral=True)
                msg =await interaction.channel.send(embed=embed)
                react = discord.utils.get(interaction.guild.emojis, name="Hardcore_Heart")
                await msg.add_reaction(react)
            else:
                embed = discord.Embed(color = 0xd14b00, description=f"Merci à **{membre.display_name}** pour avoir **boost** le serveur <a:event:1150870049222054069> <a:event:1150870049222054069>")
                await interaction.response.send_message("Le message de boost a été posté !", ephemeral=True)
                msg =await interaction.channel.send(embed=embed)
                react = discord.utils.get(interaction.guild.emojis, name="Hardcore_Heart")
                await msg.add_reaction(react)
                
        else:
            await interaction.response.send_message("Vous devez être modérateur ou administrateur pour utiliser cette commande.", ephemeral=True)


async def setup(bot):
  await bot.add_cog(Parler(bot))

  