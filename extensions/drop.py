from discord.ext import commands
import discord
from discord import app_commands
import typing
import extensions.config as config
from discord import utils as utils


def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions
def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions

class bouton_drop(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.locked = False  # Variable de verrouillage
        self.clicked_users = set()

    @discord.ui.button(label="Récupérer ",
                   style=discord.ButtonStyle.danger,
                   custom_id="recup_drop")
    async def dropper(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
        footer_original = interaction.message.embeds[0].footer.text
        nombre = int(footer_original.split()[3])
        self.nombre = nombre

        if not self.locked:
            user = interaction.user
            if user.id not in self.clicked_users:
                self.clicked_users.add(user.id)
                nb_restant = self.nombre - len(self.clicked_users)

                if nb_restant <= 0:
                    button.label = "Drop terminé 🎉"
                    button.disabled = True
                    await interaction.response.edit_message(view=self)
                    print(f"Tous les gagnants ont cliqué. Le bouton est maintenant verrouillé.")
                    
                    if nb_restant == 0:
                        embed2 = discord.Embed(color=0xd14b00, description=f"{interaction.user.mention} a gagné [le drop](https://discord.com/channels/{interaction.guild.id}/{interaction.channel.id}/{interaction.message.id}) !")
                        embed2.set_author(name='Résultat du drop', icon_url='https://i.goopics.net/xilgp9.gif')
                        await interaction.channel.send(embed=embed2)
                else:
                    if nb_restant == 1:
                        button.label = "Plus que 1 gagnant"
                    else:
                        button.label = f"Plus que {nb_restant} gagnants"

                    await interaction.response.edit_message(view=self)
                    
                    embed2 = discord.Embed(color=0xd14b00, description=f"{interaction.user.mention} a gagné [le drop](https://discord.com/channels/{interaction.guild.id}/{interaction.channel.id}/{interaction.message.id}) !")
                    embed2.set_author(name='Résultat du drop', icon_url='https://i.goopics.net/xilgp9.gif')
                    await interaction.channel.send(embed=embed2)

            else:
                await interaction.response.send_message("Vous avez déjà participé au drop!", ephemeral=True)

class Drop(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot

    # DROP
        
    @app_commands.command(description='Dropper une récompense qui doit être cliquée le plus vite possible')
    @app_commands.describe(info ="Informations à ajouter au drop",recompense="Récompense que vous souhaitez mettre en jeu", nb="Nombre de gagnants du drop")
    async def drop(self,interaction : discord.Interaction,info :typing.Optional[str], recompense : str, nb : app_commands.Range[int, 1,50]):
        cmd_use=f'\033[0;34mLa commande /drop a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m'
        print(cmd_use)
        if info == None:
            info = " "
        if is_staff(interaction.user):
            await interaction.response.send_message(f"Le drop a bien été crée dans {interaction.channel.mention}", ephemeral=True)
            embed2 = discord.Embed(color=discord.Colour(0xd14b00), title=f"Cliquez sur le bouton pour récuperer la récompense:", description=f" \n{info} \n\n > ``{recompense}``")
            if nb == 1:
                embed2.set_footer(text=f"Il y a 1 gagnant pour ce drop")
            else:
                embed2.set_footer(text=f"Il y a {nb} gagnants pour ce drop")
            await interaction.channel.send(embed=embed2, view= bouton_drop())

        else:
            await interaction.response.send_message(
                "Vous devez être modérateur ou administrateur pour utiliser cette commande.",
                ephemeral=True)


async def setup(bot):
  await bot.add_cog(Drop(bot))

  