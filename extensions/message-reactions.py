from discord.ext import commands
import discord
import extensions.config as config
from discord import utils as utils
import asyncio


def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions

def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions

user_responses = {}
last_response_time = None



class MsgReacts(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        global last_response_time
        if message.author == self.bot.user:  # Éviter que le bot réagisse à ses propres messages
            return

        contenu = message.content.lower()

        # ID des salons à exclure
        salons_exclus = config.salon_exclus_message_react

        if isinstance(message.channel, discord.DMChannel):
                user = self.bot.get_user(config.darkflav_id)
                if message.author.id == config.darkflav_id:
                    return

                await user.send(f"## Message de {message.author.display_name}:\n- {message.content}")

                if message.attachments:
                    for attachment in message.attachments:
                        file = await attachment.to_file()
                        await user.send(file=file)

                try:
                    def check(response):
                        return response.author == user and isinstance(response.channel, discord.DMChannel)

                    # Utilisez l'ID de l'auteur du message pour identifier l'utilisateur
                    user_id = message.author.id

                    # Vérifiez si l'utilisateur a déjà une liste de réponses
                    if user_id not in user_responses:
                        user_responses[user_id] = []

                    response = await self.bot.wait_for('message', check=check, timeout=2000000)

                    # Vérifiez si la réponse a déjà été traitée
                    if response.id not in user_responses[user_id]:
                        user_responses[user_id].append(response.id)

                        # Transférez la réponse de l'utilisateur (Fla) à l'utilisateur d'origine (Joie)
                        await message.author.send(f"{response.content}")

                except asyncio.TimeoutError:
                    await message.author.send("Darkflav n'a pas pu répondre, désolé. JE te laisse réecrire ta question.")

        # Réactions à certains mots-clés
        if 'hello' in message.content.lower(
        ) and message.channel.id not in salons_exclus:
            emoji = discord.utils.get(message.guild.emojis, name="Glouglou")
            await message.add_reaction(emoji)
        if message.channel.id == config.salon_notification:
            emoji1 = discord.utils.get(message.guild.emojis, name="Merci")
            emoji2 = discord.utils.get(message.guild.emojis, name="danse")
            emoji3 = discord.utils.get(message.guild.emojis, name="event")
            await message.add_reaction(emoji1)
            await message.add_reaction(emoji2)
            await message.add_reaction(emoji3)

        if 'salut' in message.content.lower(
        ) and message.channel.id not in salons_exclus:
            emoji = '👋'
            await message.add_reaction(emoji)
        if 'coucou' in message.content.lower(
        ) and message.channel.id not in salons_exclus:
            emoji = '👋'  # L'emoji que vous souhaitez ajouter
            await message.add_reaction(emoji)
        if 'bonne nuit' in message.content.lower(
        ) and message.channel.id not in salons_exclus:
            emoji = discord.utils.get(message.guild.emojis, name="pastequedodo")
            await message.add_reaction(emoji)
        if 'bn' in message.content.lower(
        ) and message.channel.id not in salons_exclus:
            emoji = discord.utils.get(message.guild.emojis, name="pastequedodo")
            await message.add_reaction(emoji)
        if '👀' in message.content.lower(
        ) and message.channel.id not in salons_exclus:
            emoji = '👀'
            await message.add_reaction(emoji)
        if message.content.lower() == '<@1162853567464476743>':
            await message.channel.send('Je suis actuellement en ligne !')



async def setup(bot):
  await bot.add_cog(MsgReacts(bot))

  