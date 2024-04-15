from discord.ext import commands
import discord
import typing
from discord import app_commands
import extensions.config as config
from discord import utils as utils


def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions
def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions

class Help(discord.ui.View):
    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

        await self.message.edit(view=self)

    @discord.ui.button(label="🏚️Accueil",
                       style=discord.ButtonStyle.grey,
                       custom_id="accueil")
    
    async def accueil(self, interaction: discord.Interaction, button):
      embed = discord.Embed(color=0xd14b00, description="Vous pouvez cliquer sur les boutons ci dessous pour choisir le type d'aide que vous souhaitez !", title="Aide pour les commandes")
      message_list = interaction.message
      await message_list.edit(embed=embed)
      await interaction.response.defer() 
    @discord.ui.button(label="🛠️ Communauté",
                       style=discord.ButtonStyle.blurple,
                       custom_id="commu")
    async def help_commu(self, interaction: discord.Interaction, button):
        message_list = interaction.message
        embed = discord.Embed(color=0xd14b00, description="Toutes les commandes liées aux autres utilisateurs")
        await message_list.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="🔊 Vocaux",
                       style=discord.ButtonStyle.green,
                       custom_id="vocaux")
    async def help_voc(self, interaction: discord.Interaction, button):
        message_list = interaction.message
        embed = discord.Embed(color=0xd14b00, description="Les différentes informations concernant les salons vocaux temporaires")
        await message_list.edit(embed=embed)
        await interaction.response.defer()

    @discord.ui.button(label="🛠️ Modération",
                       style=discord.ButtonStyle.red,
                       custom_id="mod")
    async def help_mod(self, interaction: discord.Interaction, button):
        message_list = interaction.message
        embed = discord.Embed(color=0xd14b00, description="Voici les différentes commandes de modération")
        await message_list.edit(embed=embed)
        await interaction.response.defer()

class Infos(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot

    # PDP
            
    @app_commands.command(description="Donner la photo de profil de l'utilisateur")
    @app_commands.describe(membre="Membre à qui vous souhaitez obtenir la photo de profil")
    async def pdp(self,interaction: discord.Interaction, membre: typing.Optional[discord.User] = None):
        print(f'\033[0;34mLa commande /pdp a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        if membre:
            avatar_url = membre.display_avatar
            embed= discord.Embed(color=discord.Colour(0xd14b00), description=f'[Lien direct]({avatar_url})')
            embed.set_author(name=f"Photo de profil de {membre.display_name}",icon_url='https://i.goopics.net/xilgp9.gif')
            embed.set_image(url=avatar_url)
            await interaction.response.send_message(embed=embed)
        else:
            avatar_url = interaction.user.display_avatar
            embed= discord.Embed(color=discord.Colour(0xd14b00), description=f'[Lien direct]({avatar_url})')
            embed.set_author(name=f"Photo de profil de {interaction.user.display_name}",icon_url='https://i.goopics.net/xilgp9.gif')
            embed.set_image(url=avatar_url)
            await interaction.response.send_message(embed=embed)

    # COMMANDE DE HELP

    @app_commands.command(description="Afficher la liste d'aide aux commandes")
    async def aide(self,interaction: discord.Interaction):
        print(f'\033[0;34mLa commande /help a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        embed = discord.Embed(color=0xd14b00, description="Vous pouvez cliquer sur les boutons ci dessous pour choisir le type d'aide que vous souhaitez !", title="Aide pour les commandes")
        view = Help(timeout=90)
        await interaction.response.send_message(embed=embed, view = view)
        view.message = await interaction.original_response()


async def setup(bot):
  await bot.add_cog(Infos(bot))

  