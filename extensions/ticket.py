from discord.ext import commands
import discord
import datetime
from discord import app_commands
import extensions.config as config
from discord import utils as utils
import json
import io
import asyncio
import re

def remove_markdown(text: str, guild: discord.guild) -> str:
    """Remove markdown formatting from text."""
    if re.search(r"<@\d+>",text):
       mention_all = re.findall(r"<@(\d+)>", text)
       for mention_id in mention_all:
            membre = guild.get_member(int(mention_id))
            text = text.replace(f"<@{mention_id}>", f"<span class=\"mention\">@{membre.name}</span>")
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'::', r':', text)
    

    return text


# CLASS QUI CRRE LE SALON, ET QUI VERIFIE SI PAS DE TICKET DEJA OUVERT
class ticket_launcher(discord.ui.View):
    class MonProbleme(discord.ui.Modal, title="Raison du ticket"):
        problem = discord.ui.TextInput(label="Quel est votre problème ?",placeholder="Ecrivez votre problème...", style=discord.TextStyle.long)

        def __init__(self) -> None:
          super().__init__(timeout=None)
          self.ticket_count = 0
          self.load_ticket_count()

        def save_ticket_count(self):
            with open('ticket_count.json', 'w') as file:
                json.dump({'count': self.ticket_count}, file)

        def load_ticket_count(self):
            try:
                with open('ticket_count.json', 'r') as file:
                    data = json.load(file)
                    
                    self.ticket_count = data['count']
            except (FileNotFoundError, json.JSONDecodeError):
                self.ticket_count = 0

        async def on_submit(self, interaction: discord.Interaction):
                      
            self.probleme = self.problem.value
            overwrites = {
                          interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                          interaction.user: discord.PermissionOverwrite(view_channel=True,
                                                                        send_messages=True,
                                                                        attach_files=True,
                                                                        embed_links=True),
                      }

            for role in interaction.guild.roles:
                if (role.permissions.manage_messages or role.permissions.manage_nicknames)  and not role.permissions.administrator :
                    overwrites[role] = discord.PermissionOverwrite(view_channel=True)
            if interaction.guild_id == 703325860585013249:
              category = discord.utils.get(interaction.guild.categories, id=1046487314983034910)
            elif interaction.guild_id == 1216870247995539506:
               category = discord.utils.get(interaction.guild.categories, id=1216870736153677994)
            elif interaction.guild_id == 1095449266773819462:
               category = discord.utils.get(interaction.guild.categories, id=1120756945691885618)
            ticket_name = f"Ticket-{self.ticket_count}"
            channel = await category.create_text_channel(
                          name=ticket_name,
                          overwrites=overwrites,
                          reason=f"Ticket-{self.ticket_count} pour {interaction.user}",
                          topic = f'Ticket de {interaction.user.name}')
            await interaction.response.send_message(
                          f"Un ticket a été ouvert pour vous : {channel.mention} !", ephemeral=True)

                
                      
            embed = discord.Embed(color=discord.Colour(0xd14b00), description=f"__Voici le problème de {interaction.user.mention} :__\n \n ```{self.problem}```")
            embed.set_author(name='Ticket', icon_url='https://i.goopics.net/xilgp9.gif')
            embed.set_footer(text="Le personnel vous répondra, soyez patient.\nPour fermer le ticket, réagissez avec 🔒")
            msg = await channel.send(
                          f"Bienvenue {interaction.user.mention}, la parole est à toi !",
                          embed=embed, view= main())
            await msg.pin()
            self.ticket_count += 1
            self.save_ticket_count()

                   


    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.ticket_count = 0
        self.load_ticket_count()

    def save_ticket_count(self):
        with open('ticket_count.json', 'w') as file:
            json.dump({'count': self.ticket_count}, file)

    def load_ticket_count(self):
        try:
            with open('ticket_count.json', 'r') as file:
                data = json.load(file)
                self.ticket_count = data['count']
        except (FileNotFoundError, json.JSONDecodeError):
            self.ticket_count = 0

    @discord.ui.button(label="📩 Créer un ticket",
                       style=discord.ButtonStyle.secondary,
                       custom_id="ticket_button")
    async def ticket(self, interaction: discord.Interaction,
                     button: discord.ui.Button):
        
        user_ticket = f'Ticket de {interaction.user.name}'

        # Vérifiez si un salon de texte avec le même nom existe déjà
        ticket = discord.utils.get(interaction.guild.text_channels, topic=user_ticket)

        if ticket is not None:
            await interaction.response.send_message(
                f"Vous avez actuellement un ticket d'ouvert : {ticket.mention} !",
                ephemeral=True)
        else:
            modal = self.MonProbleme()           
            await interaction.response.send_modal(modal)
            
            

      # Sauvegarde le nombre de tickets mis à jour dans le fichier JSON

# CLASS QUI DONNE LA PREMIERE POSSIBILITE DE FERMER LE SALON PAR L'UTILISATEUR
class main(discord.ui.View):

  def __init__(self) -> None:
    super().__init__(timeout=None)

  @discord.ui.button(label="🔒 Fermer",
                     style=discord.ButtonStyle.secondary,
                     custom_id="close")
  async def close(self, interaction, button):
    embed = discord.Embed(
        description="Est-tu sûr(e) de vouloir fermer ce ticket ?",
        
        color=0xd14b00)    
    await interaction.response.send_message(embed=embed,
                                            view=confirm(),
                                            ephemeral=False
                                            )

# CLASS QUI PERMET a L'UTILISATEUR DE VALIDER LA FERMETURE / D'ANNULER LA FERMETURE
class confirm(discord.ui.View):

  def __init__(self) -> None:
    super().__init__(timeout=None)

  @discord.ui.button(label=" 🔒 Fermer",
                     style=discord.ButtonStyle.danger,
                     custom_id="confirm")
  async def confirm(self, interaction: discord.Interaction, button):
    user = interaction.user
    overwrites = {
                          interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                          interaction.user: discord.PermissionOverwrite(view_channel=False,)
                      }
    for role in interaction.guild.roles:
                if (role.permissions.manage_messages or role.permissions.manage_nicknames) and not role.permissions.administrator:
                    overwrites[role] = discord.PermissionOverwrite(view_channel=True)
    await interaction.message.channel.edit(overwrites=overwrites)
    await interaction.message.delete()
    embed = discord.Embed(
        description="Merci de supprimer ce ticket s'il n'est plus utile",
        color=0xd14b00)
    embed.set_footer(text=f"Ticket clôturé par {interaction.user.display_name}")
    await interaction.channel.send(embed=embed, view=confirmation2())
    


  @discord.ui.button(label="Annuler",
                     style=discord.ButtonStyle.secondary,
                     custom_id="cancel")
  async def cancel(self, interaction, button):
    await interaction.message.delete()

# CLASS QUI PERMET AUX MODERATEURS DE REOUVRIR LE TICKET, DE LE SUPPRIMER DEFINITIVEMENT OU DE LE TRANSCRIRE
class confirmation2(discord.ui.View):
  def __init__(self) -> None:
    super().__init__(timeout=None)
  @discord.ui.button(label="🗑️ Supprimer",
                     style=discord.ButtonStyle.danger,
                     custom_id="fermer_def")
  async def fermer_def(self, interaction: discord.Interaction, button):
    embed = discord.Embed(
        description="Le ticket va être supprimé d'ici quelques secondes...",
        color=0xdb4040,
    )

    # Envoyez l'embed dans le salon du ticket
    await interaction.response.send_message(embed=embed)
    await asyncio.sleep(4)
    await interaction.channel.delete()


  @discord.ui.button(label="🔓 Réouvrir",
                     style=discord.ButtonStyle.blurple,
                     custom_id="ouvrir_def")
  async def ouvrir_def(self, interaction: discord.Interaction, button):
    channel_topic = interaction.channel.topic

    if channel_topic:
        # Séparez le nom de l'utilisateur du reste du texte (par exemple, "Ticket de User123")
        user_name_str = channel_topic[len("Ticket de "):]
        user_name = discord.utils.get(interaction.guild.members, name = user_name_str)
        utilisateur = interaction.user
        
        await interaction.channel.edit(name=f"Ticket-reouvert-{utilisateur.display_name}")
            # Mettez à jour les autorisations pour l'utilisateur
        overwrites = {
                user_name: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    attach_files=True,
                    embed_links=True
                
                ),

                interaction.guild.default_role:
        discord.PermissionOverwrite(view_channel=False),
            }
        for role in interaction.guild.roles:
               if (role.permissions.manage_messages or role.permissions.manage_nicknames) and not role.permissions.administrator:
                    overwrites[role] = discord.PermissionOverwrite(view_channel=True)
        await interaction.channel.edit(overwrites=overwrites)
        await interaction.message.delete()
        await interaction.channel.send(f"Le ticket de {user_name.mention} a été réouvert par {interaction.user.mention}.")
  @discord.ui.button(label="📁 Transcript",
                     style=discord.ButtonStyle.green,
                     custom_id="transcript")
  async def transcript(self, interaction: discord.Interaction, button):
    css = '''
        body {
            background-color: #36393e;
            color: #dcddde;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .info {
            display: flex;
            max-width: 100%;
            margin: 0 5px 10px;
        }
        .guild-icon-container {
            flex: 0;
        }
        .guild-icon {
            max-width: 88px;
            max-height: 88px;
        }
        .metadata {
            flex: 1;
            margin-left: 10px;
        }
        .guild-name {
            font-size: 1.4em;
        }
        .channel-name {
            font-size: 1.2em;
        }
        .channel-message-count {
            margin-top: 2px;
        }
        .chatlog {
            max-width: 100%;
            margin-bottom: 24px;
        }
        .message-group {
            display: flex;
            margin: 0 10px;
            padding: 15px 0;
            border-top: 1px solid;
        }
        .author-avatar-container {
            flex: 0;
            width: 40px;
            height: 40px;
        }
        .author-avatar {
            border-radius: 50%;
            height: 40px;
            width: 40px;
        }
        .messages {
            flex: 1;
            min-width: 50%;
            margin-left: 20px;
        }
        .author-name {
            font-size: 1em;
            font-weight: 500;
            font-weight: bold;
        }
        .timestamp {
            margin-left: 5px;
            font-size: 0.75em;
        }
        .message {
            padding: 2px 5px;
            margin-right: -5px;
            margin-left: -5px;
            background-color: transparent;
            transition: background-color 1s ease;
        }
        .content {
            font-size: 0.9375em;
            word-wrap: break-word;
            margin-top: 10px;
        }
        .mention {
            color: #7289da;
        }
        .embed {
            margin-top: 10px;
            background-color: #2f3136;
            border-radius: 5px;
            padding: 10px;
        }
        .embed-title {
            font-size: 1.1em;
            font-weight: bold;
            color: #fff;
            margin-bottom: 5px;
        }
        .embed-description {
            color: #dcddde;
            margin-bottom: 5px;
        }
        .embed-field {
            color: #dcddde;
            margin-bottom: 3px;
        }
        .embed-footer {
            color: #7289da;
            font-size: 0.8em;
            margin-top: 10px;
        }
    '''

    def check_message_mention(msgs: discord.Message):
        user_mentions: list = msgs.mentions
        role_mentions: list = msgs.role_mentions
        channel_mentions: list = msgs.channel_mentions
        total_mentions: list = user_mentions + role_mentions + channel_mentions
        m: str = msgs.content
        for mentions in total_mentions:
            if mentions in user_mentions:
                for mention in user_mentions:
                    m = m.replace(str(f"<@{mention.id}>"),
                                f"<span class=\"mention\">@{mention.name}</span>")
                    m = m.replace(str(f"<@!{mention.id}>"),
                                f"<span class=\"mention\">@{mention.name}</span>")
            elif mentions in role_mentions:
                for mention in role_mentions:
                    m = m.replace(str(f"<@&{mention.id}>"),
                                f"<span class=\"mention\">@{mention.name}</span>")
            elif mentions in channel_mentions:
                for mention in channel_mentions:
                    m = m.replace(str(f"<#{mention.id}>"),
                                f"<span class=\"mention\">#{mention.name}</span>")
            else:
                pass
        m = remove_markdown(m, msgs.guild)
        return m

    messages = []
    async for message in interaction.channel.history(limit=1000, oldest_first=True):
        messages.append(message)

    f = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset=utf-8>
            <meta name=viewport content="width=device-width">
            <link rel="shortcut icon" href={interaction.guild.icon.url} type="image/x-icon">
            <style>
                {css}
            </style>
        </head>
        <body>
            <div class=info>
                <div class=guild-icon-container><img class=guild-icon src={interaction.guild.icon.url}></div>
                <div class=metadata>
                    <div class=guild-name>{interaction.guild.name}</div>
                    <div class=channel-name>{interaction.channel.name}</div>
                    <div class=channel-message-count>{len(messages)} messages</div>
                </div>
            </div>
    '''

    for message in messages:
        message_contenu = message.content
        if "https://" in message_contenu and not "https://cdn.discordapp.com" in message_contenu:
            content = f"<a href=\"{message_contenu}\" class=\"mention\">{message_contenu}</a>"
        elif "<:" in message_contenu and ":" in message_contenu:
            emojis = re.findall(r"<:[a-zA-Z0-9_]+:\d+>", message_contenu)
            content = message_contenu
            for emoji in emojis:
                emoji_data = emoji.split(":")
                emoji_name = emoji_data[1]
                emoji_id = emoji_data[2][:-1]
                emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
                emoji_html = f'<img src="{emoji_url}" alt="{emoji_name}" class="emoji" width="24" height="24">'
                content = content.replace(emoji, emoji_html, 1) 
        elif message.attachments or "https://cdn.discordapp.com" in  message_contenu:
            if "https://cdn.discordapp.com" in  message_contenu:
               content = f'<img src="{message_contenu}" alt="image" width="400" height="400">'
            # IS AN IMAGE:
            elif message.attachments[0].filename.endswith(('jpg', 'png', 'gif', 'bmp')):
                if message.content:
                    content = check_message_mention(message) + '<br>' + f"<img src=\"{message.attachments[0].url}\" width=\"400\" alt=\"Attachment\" \\>"
                else:
                    content = f"<img src=\"{message.attachments[0].url}\" width=\"400\" alt=\"Attachment\" \\>"

            # IS A VIDEO
            elif message.attachments[0].filename.endswith(('mp4', 'ogg', 'flv', 'mov', 'avi')):
                if message.content:
                    content = check_message_mention(message) + '<br>' + f'''
                    <video width="320" height="240" controls>
                    <source src="{message.attachments[0].url}" type="video/{message.attachments[0].url[-3:]}">
                    Your browser does not support the video.
                    </video>
                    '''
                else:
                    content = f'''
                    <video width="320" height="240" controls>
                    <source src="{message.attachments[0].url}" type="video/{message.attachments[0].url[-3:]}">
                    Your browser does not support the video.
                    </video>
                    '''
            elif message.attachments[0].filename.endswith(('mp3', 'boh')):
                if message.content:
                    content = check_message_mention(message) + '<br>' + f'''
                    <audio controls>
                    <source src="{message.attachments[0].url}" type="audio/{message.attachments[0].url[-3:]}">
                    Your browser does not support the audio element.
                    </audio>
                    '''
                else:
                    content = f'''
                    <audio controls>
                    <source src="{message.attachments[0].url}" type="audio/{message.attachments[0].url[-3:]}">
                    Your browser does not support the audio element.
                    </audio>
                    '''
            # OTHER TYPE OF FILES
            else:
                # add things
                pass
        elif message.embeds:
            for embed in message.embeds:
                if not embed.title:
                   embed.title = ""
                if not embed.footer.text:
                   embed.footer.text =""
                embed_fields = "\n".join([f"<div class=\"embed-field\"><span class=\"markdown\">{field.name if field.name is not None else ''}</span> <span class=\"markdown\">{field.value if field.value is not None else ''}</span></div>" for field in embed.fields])
                content = f"<div class=\"embed\"><div class=\"embed-title\">{embed.title}</div><div class=\"embed-description\">{embed.description}</div>{embed_fields if embed_fields is not None else ''}<div class=\"embed-footer\">{embed.footer.text if embed.footer.text is not None else ''}</div></div>"
                serveur = message.guild
                content = remove_markdown(content, serveur)
        else:
            content = check_message_mention(message)
        
        if message.author.display_avatar == None:
            avatar_url = "https://cdn.discordapp.com/embed/avatars/1.png"
        else:
            avatar_url = message.author.display_avatar
        f += f'''
            <div class="message-group">
                <div class="author-avatar-container"><img class=author-avatar src={avatar_url}></div>
                <div class="messages">
                    <span class="author-name" >{message.author.display_name}</span><span class="timestamp">{(message.created_at + datetime.timedelta(hours=2)).strftime("%d/%m/%Y %H:%M")}</span>
                    <div class="message">
                        <div class="content"><span class="markdown">{content}</span></div>
                    </div>
                </div>
            </div>
        '''
    f += '''
            </body>
        </html>
    '''
    salon_transcript_id = config.salon_transcript

    salon_transcript = discord.utils.get(interaction.guild.channels, id=salon_transcript_id)
    await interaction.response.send_message(f"Le ticket a bien été transcrit, il est stocké dans le salon {salon_transcript.mention}")
    await salon_transcript.send(file=discord.File(fp=io.BytesIO(f.encode()), filename=f'{interaction.channel.name}.html'))  # Utilisez io.BytesIO pour les fichiers HTML


def timestamp():
        # Obtenir l'heure actuelle avec datetime.now()
        now = datetime.datetime.now()

        # Convertir l'heure actuelle en timestamp UNIX
        timestamp_unix = int(now.timestamp())

        # Envoyer le résultat
        return f"<t:{timestamp_unix}:F>"
def is_admin(user):
  # Vérifie si l'utilisateur a la permission d'administrateur
  return user.guild_permissions.administrator
def is_staff_test(user):
  required_permissions = discord.Permissions(manage_nicknames=True)
  return user.guild_permissions >= required_permissions
def is_staff(user):
  required_permissions = discord.Permissions(manage_messages=True)
  return user.guild_permissions >= required_permissions




class Ticket(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot
        

    # COMMANDE DE TICKET /AJOUTER

    @app_commands.command(description='Ajouter un membre au ticket')
    @app_commands.describe(
        utilisateur="L'utilisateur que vous voulez rajouter au ticket")
    async def ajouter(self, interaction: discord.Interaction,
                        utilisateur: discord.Member):
        print(f'\033[0;34mLa commande /ajouter a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        if "ticket-" in interaction.channel.name:
            await interaction.channel.set_permissions(utilisateur,
                                                    view_channel=True,
                                                    send_messages=True,
                                                    attach_files=True,
                                                    embed_links=True)
            await interaction.response.send_message(
                f"{utilisateur.mention} a été ajouté au ticket !")
        else:
            await interaction.response.send_message(
                'Nous ne sommes pas dans un ticket', ephemeral=True)
   
    # TICKETING

    @app_commands.command(description="Lance le système de ticket")
    async def ticketing(self,interaction: discord.Interaction):
        print(f"\033[0;34mLa commande /ticketing a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m") 
        if is_admin(interaction.user):
            embed = discord.Embed(
                title=" Besoin d'aide ?",
                description=
                "Pour créer un ticket, appuie sur 📩 sous ce message",
                color=0xd14b00)
            await interaction.response.send_message(
                "Le système de ticket a été lancé!", ephemeral=True)
            await interaction.channel.send(embed=embed, view=ticket_launcher())
            
        else:
            await interaction.response.send_message(
                "Vous devez être administrateur pour utiliser cette commande !",
                ephemeral=True)

 

    # transcript un salon

    @app_commands.command(description="Transcrire un salon")
    async def transcript(self,interaction: discord.Interaction):
        print(f'\033[0;34mLa commande /transcript a été utilisée dans {interaction.channel.name} par {interaction.user.display_name} (id : {interaction.user.id})\033[0m')
        if is_admin(interaction.user):
            await interaction.response.send_message("Transcript en cours", ephemeral=True)
            css = '''
                body {
                    background-color: #36393e;
                    color: #dcddde;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    padding: 20px;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                }
                .info {
                    display: flex;
                    max-width: 100%;
                    margin: 0 5px 10px;
                }
                .guild-icon-container {
                    flex: 0;
                }
                .guild-icon {
                    max-width: 88px;
                    max-height: 88px;
                }
                .metadata {
                    flex: 1;
                    margin-left: 10px;
                }
                .guild-name {
                    font-size: 1.4em;
                }
                .channel-name {
                    font-size: 1.2em;
                }
                .channel-message-count {
                    margin-top: 2px;
                }
                .chatlog {
                    max-width: 100%;
                    margin-bottom: 24px;
                }
                .message-group {
                    display: flex;
                    margin: 0 10px;
                    padding: 15px 0;
                    border-top: 1px solid;
                }
                .author-avatar-container {
                    flex: 0;
                    width: 40px;
                    height: 40px;
                }
                .author-avatar {
                    border-radius: 50%;
                    height: 40px;
                    width: 40px;
                }
                .messages {
                    flex: 1;
                    min-width: 50%;
                    margin-left: 20px;
                }
                .author-name {
                    font-size: 1em;
                    font-weight: 500;
                    font-weight: bold;
                }
                .timestamp {
                    margin-left: 5px;
                    font-size: 0.75em;
                }
                .message {
                    padding: 2px 5px;
                    margin-right: -5px;
                    margin-left: -5px;
                    background-color: transparent;
                    transition: background-color 1s ease;
                }
                .content {
                    font-size: 0.9375em;
                    word-wrap: break-word;
                    margin-top: 10px;
                }
                .mention {
                    color: #7289da;
                }
                .embed {
                    margin-top: 10px;
                    background-color: #2f3136;
                    border-radius: 5px;
                    padding: 10px;
                }
                .embed-title {
                    font-size: 1.1em;
                    font-weight: bold;
                    color: #fff;
                    margin-bottom: 5px;
                }
                .embed-description {
                    color: #dcddde;
                    margin-bottom: 5px;
                }
                .embed-field {
                    color: #dcddde;
                    margin-bottom: 3px;
                }
                .embed-footer {
                    color: #7289da;
                    font-size: 0.8em;
                    margin-top: 10px;
                }
            '''

            def check_message_mention(msgs: discord.Message):
                user_mentions: list = msgs.mentions
                role_mentions: list = msgs.role_mentions
                channel_mentions: list = msgs.channel_mentions
                total_mentions: list = user_mentions + role_mentions + channel_mentions
                m: str = msgs.content
                for mentions in total_mentions:
                    if mentions in user_mentions:
                        for mention in user_mentions:
                            m = m.replace(str(f"<@{mention.id}>"),
                                        f"<span class=\"mention\">@{mention.name}</span>")
                            m = m.replace(str(f"<@!{mention.id}>"),
                                        f"<span class=\"mention\">@{mention.name}</span>")
                    elif mentions in role_mentions:
                        for mention in role_mentions:
                            m = m.replace(str(f"<@&{mention.id}>"),
                                        f"<span class=\"mention\">@{mention.name}</span>")
                    elif mentions in channel_mentions:
                        for mention in channel_mentions:
                            m = m.replace(str(f"<#{mention.id}>"),
                                        f"<span class=\"mention\">#{mention.name}</span>")
                    else:
                        pass
                m = remove_markdown(m, msgs.guild)
                return m

            messages = []
            async for message in interaction.channel.history(limit=10000, oldest_first=True):
                messages.append(message)

            f = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset=utf-8>
                    <meta name=viewport content="width=device-width">
                    <link rel="shortcut icon" href={interaction.guild.icon.url} type="image/x-icon">
                    <style>
                        {css}
                    </style>
                </head>
                <body>
                    <div class=info>
                        <div class=guild-icon-container><img class=guild-icon src={interaction.guild.icon.url}></div>
                        <div class=metadata>
                            <div class=guild-name>{interaction.guild.name}</div>
                            <div class=channel-name>{interaction.channel.name}</div>
                            <div class=channel-message-count>{len(messages)} messages</div>
                        </div>
                    </div>
            '''

            for message in messages:
                message_contenu = message.content
                if "https://" in message_contenu and not "https://cdn.discordapp.com" in message_contenu:
                    content = f"<a href=\"{message_contenu}\" class=\"mention\">{message_contenu}</a>"
                elif "<:" in message_contenu and ":" in message_contenu:
                    emojis = re.findall(r"<:[a-zA-Z0-9_]+:\d+>", message_contenu)
                    content = message_contenu
                    for emoji in emojis:
                        emoji_data = emoji.split(":")
                        emoji_name = emoji_data[1]
                        emoji_id = emoji_data[2][:-1]
                        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
                        emoji_html = f'<img src="{emoji_url}" alt="{emoji_name}" class="emoji" width="24" height="24">'
                        content = content.replace(emoji, emoji_html, 1) 
                elif message.attachments or "https://cdn.discordapp.com" in  message_contenu:
                    if "https://cdn.discordapp.com" in  message_contenu:
                        content = f'<img src="{message_contenu}" alt="image" width="600" height="600">'
                    # IS AN IMAGE:
                    elif message.attachments[0].filename.endswith(('jpg', 'png', 'gif', 'bmp')):
                        if message.content:
                            content = check_message_mention(message) + '<br>' + f"<img src=\"{message.attachments[0].url}\" width=\"600\" alt=\"Attachment\" \\>"
                        else:
                            content = f"<img src=\"{message.attachments[0].url}\" width=\"600\" alt=\"Attachment\" \\>"

                    # IS A VIDEO
                    elif message.attachments[0].filename.endswith(('mp4', 'ogg', 'flv', 'mov', 'avi')):
                        if message.content:
                            content = check_message_mention(message) + '<br>' + f'''
                            <iframe style="margin-left: 30px; box-shadow: 6px 6px 10px grey;" src="{message.attachments[0].url}" frameborder="0" width="500" height="281"></iframe>
                            '''
                        else:
                            content = f'''
                            <iframe style="margin-left: 30px; box-shadow: 6px 6px 10px grey;" src="{message.attachments[0].url}" frameborder="0" width="500" height="281"></iframe>
                            '''
                    elif message.attachments[0].filename.endswith(('mp3', 'boh')):
                        if message.content:
                            content = check_message_mention(message) + '<br>' + f'''
                            <audio controls>
                            <source src="{message.attachments[0].url}" type="audio/{message.attachments[0].url[-3:]}">

                            </audio>
                            '''
                        else:
                            content = f'''
                            <audio controls>
                            <source src="{message.attachments[0].url}" type="audio/{message.attachments[0].url[-3:]}">
                            </audio>
                            '''
                    # OTHER TYPE OF FILES
                    else:
                        # add things
                        pass
                elif message.embeds:
                    for embed in message.embeds:
                        if not embed.title:
                            embed.title = ""
                        if not embed.footer.text:
                            embed.footer.text =""
                        embed_fields = "\n".join([f"<div class=\"embed-field\"><span class=\"markdown\">{field.name if field.name is not None else ''}</span> <span class=\"markdown\">{field.value if field.value is not None else ''}</span></div>" for field in embed.fields])
                        content = f"<div class=\"embed\"><div class=\"embed-title\">{embed.title}</div><div class=\"embed-description\">{embed.description}</div>{embed_fields if embed_fields is not None else ''}<div class=\"embed-footer\">{embed.footer.text if embed.footer.text is not None else ''}</div></div>"
                        serveur = message.guild
                        content = remove_markdown(content, serveur)
                else:
                    content = check_message_mention(message)
                
                if message.author.display_avatar == None:
                    avatar_url = "https://cdn.discordapp.com/embed/avatars/1.png"
                else:
                    avatar_url = message.author.display_avatar
                f += f'''
                    <div class="message-group">
                        <div class="author-avatar-container"><img class=author-avatar src={avatar_url}></div>
                        <div class="messages">
                            <span class="author-name" >{message.author.display_name}</span><span class="timestamp">{(message.created_at + datetime.timedelta(hours=2)).strftime("%d/%m/%Y %H:%M")}</span>
                            <div class="message">
                                <div class="content"><span class="markdown">{content}</span></div>
                            </div>
                        </div>
                    </div>
                '''
            f += '''
                    </body>
                </html>
            '''
            salon_transcript_id = config.salon_transcript
            salon_transcript = self.bot.get_channel(salon_transcript_id)
            await interaction.followup.send(f"Le ticket a bien été transcrit, il est stocké dans le salon {salon_transcript.mention}", ephemeral=True)
            await salon_transcript.send(file=discord.File(fp=io.BytesIO(f.encode()), filename=f'{interaction.channel.name}.html'))  # Utilisez io.BytesIO pour les fichiers HTML

        else:
            await interaction.response.send_message(
                "Vous devez être administrateur pour utiliser cette commande !",
                ephemeral=True)


async def setup(bot):
  await bot.add_cog(Ticket(bot))



  