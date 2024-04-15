from discord.ext import commands
import discord
from discord import app_commands
import extensions.config as config
from discord import utils as utils
import nacl



def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions

def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions




class Voice(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        serveur = self.bot.get_guild(config.serveur_voc_delete)
        for salon in serveur.channels:
            if salon.name.startswith('🔊・'):
                        if len(salon.members) == 0:
                            await salon.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        specific_channel_id = config.salon_creer_voc
        serveur = member.guild
        for salon in serveur.channels:
            if salon.name.startswith('🔊・'):
                if len(salon.members) == 0:
                    await salon.delete()
        if after.channel and after.channel.id == specific_channel_id:
            categorie =  discord.utils.get(serveur.categories, id=config.categorie_creer_vocal)
            overwrites = {
                            member: discord.PermissionOverwrite(use_application_commands=True,
                                                                            send_messages=True)
                        }
            salon = await categorie.create_voice_channel(
                            name=f"🔊・{member.name}",overwrites=overwrites)
            await salon.edit(user_limit=20)
            await member.move_to(salon)



    # INVITE LAYLO SUPPORT EN VOC
  
    @app_commands.command(description="Inviter Laylo Support en vocal")
    async def join(self,interaction: discord.Interaction):
        print(f'\033[0;34mLa commande /join a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        # Vérifiez si l'utilisateur a rejoint un canal vocal
        if interaction.user.voice.channel:
            channel = interaction.user.voice.channel
            await interaction.response.send_message("J'ai bien été ajouté à votre salon vocal ! Je ne peux pas vous parler, mais je vous tiendrai compagnie 🤗")
            await channel.connect()
            
        else:
            await interaction.response.send_message("Vous devez rejoindre un salon vocal avant d'utiliser cette commande.", ephemeral=True)
    
            
    # VOICE LIMITE

    @app_commands.command(description="Modifier la limite du salon")
    @app_commands.describe(nombre="La limite de membres que vous voulez mettre sur le vocal (0 : aucune limite)")
    async def voice_limit(self,interaction : discord.Interaction,nombre: app_commands.Range[int, 0,99]):
        print(f'\033[0;34mLa commande /voice_limit a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        if interaction.user.voice:
            vocal = interaction.user.voice.channel
            if vocal.name.startswith('🔊・'):
                if str(interaction.user.voice.channel) == str(f"🔊・{interaction.user.name}"):
                    if nombre == 0:
                        await vocal.edit(user_limit=None)
                        await interaction.response.send_message("La limite de membres a bien été supprimée !", ephemeral=True)
                    else:
                        await vocal.edit(user_limit=nombre)
                        await interaction.response.send_message("La limite de membres a bien été modifiée !", ephemeral=True)
                else:
                    await interaction.response.send_message("Vous n'êtes pas le propriétaire du vocal !", ephemeral=True)
            else:
                await interaction.response.send_message("Vous devez être dans un salon vocal temporaire !", ephemeral=True)
        else:
            await interaction.response.send_message("Vous devez être dans un salon vocal !", ephemeral=True)

    # VOICE KICK

    @app_commands.command(description="Expulser un membre du salon vocal")
    @app_commands.describe(membre="Le membre que vous souhaitez expulser")
    async def voice_kick(self,interaction : discord.Interaction,membre: discord.Member):
        print(f'\033[0;34mLa commande /voice_kick a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        if is_staff_test(membre):
            await interaction.response.send_message(f"Vous ne pouvez pas expulser du vocal {membre.mention}, car il a des permissions de modérations", ephemeral=True)
        else:
            if interaction.user.voice:
                if membre.voice:
                    if str(interaction.user.voice.channel) == str(membre.voice.channel):
                        if str(interaction.user.voice.channel) == str(f"🔊・{interaction.user.name}"):
                            overwrites = {
                                            interaction.user: discord.PermissionOverwrite(use_application_commands=True,
                                                                                        send_messages=True),
                                            membre: discord.PermissionOverwrite(connect=False,send_messages = False)
                                                                                        
                                        }
                            salon_voc=membre.voice.channel
                            await salon_voc.edit(overwrites=overwrites)
                            await membre.move_to(None)
                            await interaction.response.send_message(f"{membre.mention} a été expulsé du vocal et ne pourra plus rejoindre. Pour lui redonner l'accès, utilisez /voice_add" ,ephemeral=True)
                        else:
                            await interaction.response.send_message("Vous n'êtes pas le propriétaire du vocal !", ephemeral=True)
                    else:
                        await interaction.response.send_message(f"{membre.mention} n'est pas dans le même salon vocal que vous !", ephemeral=True)
                else:
                    await interaction.response.send_message(f"{membre.mention} n'est pas dans un salon vocal !", ephemeral=True)
            else:
                await interaction.response.send_message("Vous n'êtes pas dans un salon vocal !", ephemeral=True)
            

    # VOICE DELETE

    @app_commands.command(description="Supprimer votre salon vocal temporaire")
    async def voice_delete(self, interaction :discord.Interaction):
        print(f'\033[0;34mLa commande /voice_delete a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        if interaction.user.voice:
            if str(interaction.user.voice.channel) == str(f"🔊・{interaction.user.name}"):
                await interaction.response.send_message(f"Votre salon vocal a bien été supprimé !" ,ephemeral=True)
                await interaction.user.voice.channel.delete()
            else:
                await interaction.response.send_message("Vous n'êtes pas le propriétaire du vocal !", ephemeral=True)
        else:
            await interaction.response.send_message("Vous n'êtes pas dans un salon vocal !", ephemeral=True)


async def setup(bot):
  await bot.add_cog(Voice(bot))

  