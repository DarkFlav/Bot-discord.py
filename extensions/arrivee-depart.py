from discord.ext import commands
import discord
import extensions.config as config
from discord import utils as utils


def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions

def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions




class Arrivee(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
       guild = self.bot.get_guild(
      config.serveur_membre)
       if guild:
        member_count_channel = discord.utils.get(guild.channels,
                                             id=config.salon_comptage_membres)
        if member_count_channel:
            member_count = len(guild.members)
            
            await member_count_channel.edit(name=f'Membres : {member_count}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(config.serveur_membre)
        if guild:
            activity = discord.Activity(
            name=f"{len(guild.members)} membres ",
            type=discord.ActivityType.watching,

        )
            await self.bot.change_presence(activity=activity)

            member_count_channel = discord.utils.get(guild.channels,
                                                id=config.salon_comptage_membres)
            if member_count_channel:
                member_count = len(guild.members)
                
                await member_count_channel.edit(name=f'Membres : {member_count}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.bot.get_guild(config.serveur_membre)
        if guild:
            activity = discord.Activity(
            name=f"{len(guild.members)} membres ",
            type=discord.ActivityType.watching,

        )
            await self.bot.change_presence(activity=activity)
            member_count_channel = discord.utils.get(guild.channels,
                                                id=config.salon_comptage_membres)
            if member_count_channel:
                member_count = len(guild.members)
                
                await member_count_channel.edit(name=f'Membres : {member_count}')


async def setup(bot):
  await bot.add_cog(Arrivee(bot))

  