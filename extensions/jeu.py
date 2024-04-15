from discord.ext import commands
import discord
import datetime
import random
from discord import app_commands
import extensions.config as config
from discord import utils as utils
import requests
from googletrans import Translator



def translate_country_name(country_name):
    try:
        translator = Translator()
        translation = translator.translate(country_name, src='en', dest='fr')
        return translation.text
    except Exception as e:
        print(e)
        return country_name

class Jeu(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot

    #  NOMBRE ALEATOIRE ENTRE DEUX NOMBRES DONNEES

    @app_commands.command(description="Donner un nombre aléatoire entre deux nombres")
    @app_commands.describe(min ="Donnez un nombre minimum", max ="Donnez un nombre maximum")
    async def nombre_aleatoire(self, interaction: discord.Interaction, min: int,
                                max: int):
        print(f'\033[0;34mLa commande /nombre_random a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        
        if min >= max:
            await interaction.response.send_message(
                "Le nombre minimum doit être inférieur au nombre maximum.",
                ephemeral=True)
        else:
            random_value = random.randint(min, max)
            await interaction.response.send_message(
                f"Nombre aléatoire entre {min} et {max} : {random_value}")

    # PILE OU FACE

    @app_commands.command(description="Pile ou face avec une pièce")
    async def pile_ou_face(self, interaction: discord.Interaction):
        print(f'\033[0;34mLa commande /pile_ou_face a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        resultat = random.choice(["pile", "face"])
        await interaction.response.send_message(f"Le résultat est : {resultat}")
            
        


    # METEO
    
    @app_commands.command(description="Donner la météo de la ville de votre choix")
    @app_commands.describe(ville="La ville dont vous souhaitez la météo")
    async def meteo(self, interaction:discord.Interaction, ville : str):
        print(f'\033[0;34mLa commande /meteo {ville} a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        try:
                base_url = config.API_METEO
                complete_url = f"{base_url}&q={ville}&lang=fr"
                response = requests.get(complete_url)
                result = response.json()

                city_name = result['location']['name']
                country = result['location']['country']
                time = result['location']['localtime']
                wcond = result['current']['condition']['text']
                celcius = result['current']['temp_c']
                fclike = result['current']['feelslike_c']
                localtime_obj = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
                localtime_formatted = localtime_obj.strftime("%d/%m/%Y ・ %H:%M")
                country_name = translate_country_name(country)

                embed = discord.Embed(title=f"Météo à {city_name}", description=f"Pays: {country_name}", color=0xd14b00)
                embed.add_field(name="Température", value=f"{celcius}°C", inline=True)
                embed.add_field(name="Température ressentie ", value=f"{fclike}°C", inline=True)
                embed.add_field(name="Conditions météorologiques", value=f"{wcond}", inline=False)
                embed.set_footer(text=f"Heure locale: {localtime_formatted}")

                await interaction.response.send_message(embed=embed)
        except Exception as e:
                await interaction.response.send_message("Il y a eu un problème avec le nom de la ville, vous devez le donnez dans la langue du pays dans laquel elle est", ephemeral=True)

async def setup(bot):
  await bot.add_cog(Jeu(bot))

  