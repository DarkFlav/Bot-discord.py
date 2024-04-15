from discord.ext import commands
import discord
from discord import app_commands
import extensions.config as config
from discord import utils as utils


def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions

class Sondage(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot

        # SONDAGE
    @app_commands.command(description="Créer un sondage avec une question et des réponses possibles")
    @app_commands.describe(question="Posez une question",reponses = "Mettez les réponses en les séparant avec un /")
    async def sondage(self,interaction: discord.Interaction, question: str,
                    reponses: str):
        cmd_use = f'\033[0;34mLa commande /sondage a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)

        if is_staff(interaction.user):
            reponses_list = reponses.split('/')

            if len(reponses_list) < 2:
                await interaction.response.send_message(
                "Veuillez spécifier au moins deux réponses pour le sondage.",
                ephemeral=True)
            else:
                await interaction.response.send_message("Le sondage a bien été envoyé !",
                                                        ephemeral=True)
                message = f"```{question}```\n\n**Votez pour une réponse :**"
                embed=discord.Embed(color=0xd14b00, title="Sondage")
                for i, reponse in enumerate(reponses_list):
                    message += f"\n{i}. {reponse.strip()}"
                embed.description=message  

                poll_message = await interaction.channel.send(embed=embed)
                for i in range(1, len(reponses_list) + 1):
                    await poll_message.add_reaction(f"{i}\N{COMBINING ENCLOSING KEYCAP}")
        else:
            await interaction.response.send_message(
                "Vous devez être modérateur ou administrateur pour utiliser cette commande.",
                ephemeral=True)

    #CLOTURER UN SONDAGE

    @app_commands.command(description="Clôturer un sondage déja existant")
    @app_commands.describe(identifiant='Identifiant discord du sondage à clôturer')
    async def cloturer(self,interaction: discord.Interaction, identifiant: str):
        cmd_use = f'\033[0;34mLa commande /cloturer a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)
        if is_staff(interaction.user):
            try:
                # Récupérez le message de sondage en fonction de son ID
                poll_message = await interaction.channel.fetch_message(identifiant)
                await interaction.response.send_message(
                    "Le sondage a bien été clôturé !", ephemeral=True)
                # Calculez les résultats en comptant les réactions
                total_votes = sum([
                    reaction.count - 1 for reaction in poll_message.reactions
                ])  # Soustrayez 1 pour exclure le bot
                results = {}
                for reaction in poll_message.reactions:
                    option = reaction.emoji
                    vote_count = reaction.count - 1  # Soustrayez 1 pour exclure le bot
                    percentage = (vote_count / total_votes) * 100
                    results[
                        option] = f"{percentage:.2f}% des votants préfèrent la réponse "

                # Annoncez les résultats
                result_message = "**Les résultats sont **:\n"
                for option, percentage in results.items():
                    result_message += f"- {percentage} {option}\n"

                await interaction.channel.send(result_message)

            except discord.NotFound:
                await interaction.response.send_message(
                    "Le message n'a pas été trouvé !", ephemeral=True)
        else:
            await interaction.response.send_message(
                "Vous devez être modérateur ou administrateur pour utiliser cette commande.",
                ephemeral=True)

            
        

async def setup(bot):
  await bot.add_cog(Sondage(bot))

  