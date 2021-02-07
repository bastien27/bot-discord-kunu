# -----Start-----------------------------------------------------------------
import urllib.request
import discord
import sqlite3
import valve.source
import valve.source.a2s
import valve.source.master_server
import json
import asyncio

from discord.ext import commands


bot = commands.Bot(command_prefix="!")
bot.remove_command("help")
connection = sqlite3.connect("data.db")


# Event ----------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f"{bot.user.display_name} is on-line")
    await bot.change_presence(activity=discord.Game("essayer de vous aidé :)"))


# @bot.event
# async def on_command_error(ctx, errtxt):
#    print(on_command_error)
#    print(errtxt)
#    await ctx.send(errtxt)


# on message
@bot.event
async def on_message(message):
    # id tribe kunu
    if message.channel.id == 805017522625445899:
        try:
            c_addmem = connection.cursor()
            addmemberlist = message.content.splitlines()
            memdiscnam = f"{message.author.name}#{message.author.discriminator}"
            memberitemlist = [c_addmem.lastrowid, str(message.author.id), memdiscnam]
            for addmemberitem in addmemberlist:
                addmemitem = addmemberitem.split(':')
                memberitemlist.append(addmemitem[1].strip())
            memberitemlist.append("")
            memberitemlist.append("")
            print(memberitemlist)
            c_addmem.execute('INSERT INTO kunu_membre VALUES (?,?,?,?,?,?,?,?,?,?,?)', memberitemlist)
            connection.commit()
            c_addmem.close()
            await message.channel.send("votre id est enregistrer correctement")
        except:
            await message.channel.send("Merci de copier/coller et de remplir le formulaire ci-dessous.\nNE SUPPRIMER RIEN, ajouté seulement les informations necessaires\nsi vous avez plusieurs avatars, séparer chaques nom par une virgule\n\nSteam ID64 :\nSteam name :\nEpic ID :\nEpic name :\nNom(s) d'avatar(s) :\nHistorique/Description :")
        print(message)
    await bot.process_commands(message)


async def creatvoicechannel(guild, channelname, categoryid=807415683901554729):
    category = categorybyid(guild, categoryid)
    await guild.create_voice_channel(channelname, category=category)
    channel = channelbyname(guild, channelname)
    return channel


def categorybyid(guild, categoryid):
    category = None
    for c in guild.categories:
        if c.id == categoryid:
            category = c
            break
    return category


def channelbyname(guild, channelname):
    channel = None
    for c in guild.channels:
        if c.name == channelname:
            channel = c
            break
    return channel

# salon vocal automatique
@bot.event
async def on_voice_state_update(memberudvoice, voicebefore, voiceafter):
    try:
        if voiceafter.channel is not None:
            if voiceafter.channel.id == 807661010429149204:
                channel = await creatvoicechannel(voiceafter.channel.guild, f'Vocal de {memberudvoice.name}')
                if channel is not None:
                    await memberudvoice.move_to(channel)
    except:
        return
    try:
        if voicebefore.channel.id != 807661010429149204 and voicebefore.channel is not None:
            if voicebefore.channel.category.id == categorybyid(voicebefore.channel.guild, 807415683901554729).id:
                if len(voicebefore.channel.members) == 0:
                    await voicebefore.channel.delete()
    except:
        return


# -----Authorisation----------------------------------------------------------
def kunu_chan():
    def predicate(ctx):
        return ctx.channel.id == 681588910018920560 or ctx.message.author.id == 178805129984606208
    return commands.check(predicate)


def kunu_admin():
    def predicate(ctx):
        return ctx.channel.id == 692172772645929031 or ctx.message.author.id == 178805129984606208
    return commands.check(predicate)


def trib_chan():
    def predicate(ctx):
        return ctx.channel.id == 805116373843968001 or ctx.message.author.id == 178805129984606208
    return commands.check(predicate)


def trib_admin():
    def predicate(ctx):
        print(ctx.author.roles)
        for role in ctx.author.roles:
            if str(role) == str("Admin") or ctx.message.author.id == 178805129984606208:
                return True
    return commands.check(predicate)


def onlyme(ctx):
   return ctx.message.author.id == 178805129984606208


def trib_core():
    def predicate(ctx):
        print(ctx.author.roles)
        for role in ctx.author.roles:
            if str(role) == str("Admin") or str(role) == str("Core") or ctx.message.author.id == 178805129984606208:
                return True
    return commands.check(predicate)


# -----data-------------------------------------------------------------------
reqrate = urllib.request.urlopen("http://arkdedicated.com/dynamicconfig.ini")
datrate = reqrate.read().decode('utf-8')
reqnotif = urllib.request.urlopen("http://arkdedicated.com/pcnotification.html")
pcnotif = reqnotif.read().decode('utf-8')
reqnews = urllib.request.urlopen("http://arkdedicated.com/news.ini")
pcnews = reqnews.read().decode('utf-8')
reqclust = urllib.request.urlopen("http://arkdedicated.com/officialtributeenabled.html")
infoclust = str(reqclust.read().decode('utf-8'))
reqstatus = urllib.request.urlopen("http://arkdedicated.com/officialserverstatus.ini")
pcstatus = reqstatus.read().decode('utf-8')
reqmobdb = urllib.request.urlopen("http://arkdedicated.com/mobile/cache/officialserverlist.json")
mobdb = json.load(reqmobdb)
reqxbdb = urllib.request.urlopen("http://arkdedicated.com/xbox/cache/officialserverlist.json")
xbdb = json.load(reqxbdb)
reqxbudb = urllib.request.urlopen("http://arkdedicated.com/xbox/cache/unofficialserverlist.json")
xbudb = json.load(reqxbudb)
reqswidb = urllib.request.urlopen("http://arkdedicated.com/switch/cache/officialserverlist.json")
swidb = json.load(reqswidb)
reqswiudb = urllib.request.urlopen("http://arkdedicated.com/switch/cache/unofficialserverlist.json")
swiudb = json.load(reqswiudb)
reqban = urllib.request.urlopen("http://arkdedicated.com/banlist.txt")
datban = reqban.read().decode('utf-8')

colr1 = ("1, 0, 0, 1", 0xff0000)
colr2 = ("0.2, 1, 1, 1", 0x00ffff)
colr3 = ("0.9, 0.9, 0.9, 1", 0x909090)
colr4 = ("1, 0.5 ,1 ,1", 0xff77ff)
colr5 = ("1, 1, 1, 1", 0xffffff)
colr6 = ("0, 1, 0, 1", 0x00ff00)
notiftest = ".."

prim = (0xb3b3b3, 'primitive')
ram = (0x33FF33, 'ramshackle')
app = (0x334CFF, 'apprentice')
jour = (0x7F33FF, 'journeyman')
mast = (0xFFF319, 'mastercraft')
asc = (0x00FFFF, 'ascendant')

c_bpdat = connection.cursor()
databp = c_bpdat.execute(f'SELECT * FROM bp_dat')
bpdatlist = []
for bpdata in databp.fetchall():
    bpdatlist.append(bpdata)
c_bpdat.close()


# -----Help---------------------------------------------------
@bot.group(invoke_without_command=True)
async def help(ctx):
    # traitement embed
    embedhelp = discord.Embed(title="Help", description="Use !help <command> for extended information on a commande.")
    embedhelp.add_field(name="BP", value="bp -> show a BP in the DataBase \nbp_list -> show all bp type recorded in DataBase\nbp_craft -> calc. of the resources required for a bp", inline=True)
    embedhelp.add_field(name="Tools", value="rate -> show actual rate\nban -> show if steamid is banned of official server\nabout -> about the bot", inline=True)
    await ctx.send(embed=embedhelp)


@help.command()
async def bp(ctx):
    embedhbp = discord.Embed(title="Help -> !bp", description="Show a BP in the DataBase, you can use !bp_list for show all bp type recorded.")
    embedhbp.add_field(name="Syntax",
                        value="!bp <type bp>", inline=False)
    embedhbp.add_field(name="Example",
                        value="!bp Giga ; !bp MDSM ; !bp hatchet",
                        inline=False)
    await ctx.send(embed=embedhbp)


@help.command()
async def bp_craft(ctx):
    embedhelp = discord.Embed(title="Help -> !bp_craft", description="calculations the resources needed to craft a bp a given quantity")
    embedhelp.add_field(name="Syntax",
                        value="!bp_craft <bp id> [quantity]", inline=False)
    embedhelp.add_field(name="Example for craft x17 bp number 124",
                        value="!bp_craft 124 17",
                        inline=False)
    await ctx.send(embed=embedhelp)


@help.command()
async def ban(ctx):
    embedhelp = discord.Embed(title="Help -> !ban", description="show if steamid is banned of official server")
    embedhelp.add_field(name="Syntax",
                        value="!ban <steamid64>", inline=False)
    embedhelp.add_field(name="Example",
                        value="!ban 1234567890987654321",
                        inline=False)
    await ctx.send(embed=embedhelp)


# Tools-----------------------------------------------------------------------------------------------------------------
version = '2.0'
date = '2021/02/03'
@bot.command()
async def about(ctx):
    embedvar = discord.Embed(title="A Propos", description="A propos du bot et du serveur",
                             color=0x000000)
    embedvar.set_thumbnail(url="https://cdn.discordapp.com/attachments/758286318996029440/806606862152630292/logokunubot_trans.png")
    embedvar.add_field(name="A propos du bot", value="Bot développer EXCLUSIVEMENT pour le serveur Discord KUNU", inline=False)
    embedvar.add_field(name="Developer en python", value="par Bastien27 d'après une idée de Sémix", inline=False)
    embedvar.add_field(name="Version", value=version, inline=False)
    embedvar.add_field(name="Date Realase", value=date, inline=False)
    embedvar.add_field(name="Besoins d'aides", value="utiliser la commande \"!help\" pour plus d'aide", inline=False)
    embedvar.add_field(name="A propos du serveur", value="Serveur communautaire FR Ark - KUNU", inline=False)
    embedvar.add_field(name="Proprietaire", value=ctx.guild.owner, inline=False)
    embedvar.add_field(name="creer le", value=ctx.guild.created_at, inline=False)
    embedvar.add_field(name=f"{len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)} salons sur le serveur", value=f"{len(ctx.guild.text_channels)} salons textuels\n{len(ctx.guild.voice_channels)} salons vocal", inline=False)
    embedvar.add_field(name="actuellement connecter sur la région", value=f"{ctx.guild.region}", inline=False)
    embedvar.add_field(name="membres actuel", value=ctx.guild.member_count, inline=False)
    await ctx.channel.send(embed=embedvar)
    print('about asked')


@bot.command()
@kunu_chan()
async def infoserv(ctx):
    creat = discord.Guild.created_at
    await ctx.send(creat)
    nummember = discord.Guild.member_count
    await ctx.send(nummember)


# -----Three-Eyed Crow--------------------------------------------------------------------------------------------------


# -----Query server-----------------------------------------------------------------------------------------------------

@bot.command()
@trib_chan()
async def query(ctx, map):
    address = []
    playernameview = []
    playertimeview = []
    if int(map) == 793:
        address.append("46.251.238.161")
        address.append(27019)
    if int(map) == 252:
        address.append("85.190.155.193")
        address.append(27017)
    if int(map) == 484:
        address.append("5.101.166.198")
        address.append(27019)
    if int(map) == 676:
        address.append("85.190.155.152")
        address.append(27015)
    with valve.source.a2s.ServerQuerier(address, timeout=20) as query:
        players = []
        playercountview = f"{query.info()['player_count']}/{query.info()['max_players']}"
        mapview = query.info()["map"]
        servernameview = query.info()["server_name"]
        for player in query.players()["players"]:
            print(player["name"])
            print(player["duration"])
            playernameview.append(player['name'])
            playertimeview.append(str(player['duration']))
            if player["name"]:
                players.append(player)
        player_count = len(players)
        rulesview = query.rules()["rules"]
    embedhbp = discord.Embed(title="Info serveur", description=servernameview)
    embedhbp.add_field(name="map",
                        value=mapview, inline=True)
    embedhbp.add_field(name="joueurs",
                        value=playercountview,
                        inline=True)
    embedhbp.add_field(name="joueurs steam",
                       value=f"{player_count}",
                       inline=True)
    dlavatar = ''
    dlitem = ''
    if int(rulesview["ALLOWDOWNLOADCHARS_i"]) == 1:
        dlavatar = "Avatar autorisé"
    else:
        dlavatar = "Transfert avatar désactivé"
    if int(rulesview["ALLOWDOWNLOADITEMS_i"]) == 1:
        dlitem = "Item autorisé"
    else:
        dlitem = "Transfert item désactivé"
    embedhbp.add_field(name="Transfert",
                       value=f"{dlavatar}\n{dlitem}",
                       inline=True)
    embedhbp.add_field(name="Cluster ID",
                       value=rulesview["ClusterId_s"],
                       inline=True)
    embedhbp.add_field(name="jours in-game",
                       value=rulesview["DayTime_s"],
                       inline=True)
    embedhbp.add_field(name="joueur connecté", value="\n".join(playernameview), inline=True)
    embedhbp.add_field(name="temps de connection\n(en second)", value="\n".join(playertimeview), inline=True)
    await ctx.send(embed=embedhbp)


# -----Outils-----------------------------------------------------------------------------------------------------------
# info network
@bot.command()
@kunu_chan()
async def infopc(ctx):
    pcinfo = f"{pcnotif}\n{pcstatus}\n{pcnews}"
    pcinfo1 = pcinfo.replace(">", "\n")
    pcinfo2 = pcinfo1.replace("<", "\n")
    pcinfo3 = pcinfo2.replace("\"", "\n")
    infopc = pcinfo3.splitlines()
    if infoclust == '1':
        clustinfo = "connecté"
    else:
        clustinfo = "déconnecté"
    colorstatus = colr1[1]
    if infopc[3] != '':
        if infopc[3] == colr1[0]:
            colorstatus = colr1[1]
        if infopc[3] == colr2[0]:
            colorstatus = colr2[1]
        if infopc[3] == colr3[0]:
            colorstatus = colr3[1]
        if infopc[3] == colr4[0]:
            colorstatus = colr4[1]
        if infopc[3] == colr5[0]:
            colorstatus = colr5[1]
        if infopc[3] == colr6[0]:
            colorstatus = colr6[1]
    # traitement embed
    embedinfo = discord.Embed(title="Info Wildcard PC",
                              description=f"Status : {infopc[5]}\nCluster transfert = {clustinfo}", color=colorstatus)
    if infopc[0] != notiftest:
        embedinfo.add_field(name="Info :", value=infopc[0], inline=False)
    embedinfo.add_field(name="Wilcard News",
                        value=f"{infopc[19]}\n\n{infopc[27]}\n{infopc[33]}\n\n{infopc[41]}\n{infopc[47]}", inline=False)
    print("info WC demandé")
    await ctx.channel.send(embed=embedinfo)


@bot.command()
@kunu_chan()
async def info(ctx, devise, srvquery):
    embeddat = ['', 'NOK', 'NOK', '', '', '', '', '', 'non', '', '', '', '', '', '']
    if str.lower(devise) == "mobile":
        for servm in mobdb:
            if servm['IP'] == srvquery:
                cluserm = servm['ClusterId']
                print(cluserm, servm['AllowDownloadItems'], servm['Name'], servm['Region'], servm['IP'], servm['NPEnvironment'], servm['MinorBuildId'], servm['MaxPlayers'],  servm['MapName'], servm['SessionIsPve'], servm['NPSessionId'], servm['AllowDownloadChars'], servm['NumPlayers'], servm['LastUpdated'], servm['BuildId'], servm['Port'], servm['DayTime'], servm['GameMode'])
    if str.lower(devise) == "xbox":
        for servxb in xbdb:
            if str.lower(srvquery) in str.lower(servxb['Name']):
                embeddat[0] = servxb['Name']
                embeddat[3] = f"{servxb['IP']}:{servxb['Port']}"
                embeddat[4] = f"{servxb['BuildId']}.{servxb['MinorBuildId']}"
                embeddat[5] = f"{servxb['NumPlayers']}/{servxb['MaxPlayers']}"
                embeddat[6] = servxb['ClusterId']
                embeddat[7] = servxb['MapName']
                embeddat[9] = servxb['LastUpdated']
                embeddat[10] = servxb['DayTime']
                if servxb['AllowDownloadItems'] == 1:
                    embeddat[1] = 'OK'
                if servxb['AllowDownloadChars'] == 1:
                    embeddat[2] = 'OK'
                if servxb['SessionIsPve'] == 1:
                    embeddat[8] = 'oui'
                embedinfos = discord.Embed(title=f"Info pour serveur {str.lower(devise)}", description=embeddat[0], color=0x00ff00)
                embedinfos.add_field(name="Téléchargement", value=f"Item {embeddat[1]}\nCharactère {embeddat[2]}", inline=True)
                embedinfos.add_field(name="IP", value=embeddat[3], inline=True)
                embedinfos.add_field(name="Version", value=embeddat[4], inline=True)
                embedinfos.add_field(name="Joueurs", value=embeddat[5], inline=True)
                embedinfos.add_field(name="Cluster Id", value=embeddat[6], inline=True)
                embedinfos.add_field(name="Map", value=embeddat[7], inline=True)
                embedinfos.add_field(name="PvE", value=embeddat[8], inline=True)
                embedinfos.add_field(name="Dernière MàJ", value=embeddat[9], inline=True)
                embedinfos.add_field(name="Nombres de jours in-game", value=embeddat[10], inline=True)
                await ctx.channel.send(embed=embedinfos)
        await ctx.send(":white_check_mark:")


# Rate
@bot.command()
async def rate(ctx):
    # traitement phrase description
    ratedat = datrate.replace("=", "\n")
    ratelist = ratedat.splitlines()
    viewrate = ['', '', '', '']
    baserate = ['1.0']
    if ratelist[1] == baserate[0] and ratelist[3] == baserate[0] and ratelist[5] == baserate[0] and ratelist[7] == \
            baserate[0] and ratelist[9] == baserate[0] and ratelist[11] == baserate[0] and ratelist[13] == baserate[0] \
            and ratelist[15] == baserate[0] and ratelist[17] == baserate[0]:
        viewrate[0] = 'aucun '
        viewrate[1] = 'event '
    if ratelist[1] != baserate[0] or ratelist[3] != baserate[0] or ratelist[5] != baserate[0] or ratelist[7] != \
            baserate[0] or ratelist[9] != baserate[0] or ratelist[11] != baserate[0] or ratelist[13] != baserate[0] or \
            ratelist[15] != baserate[0] or ratelist[17] != baserate[0]:
        viewrate[1] = 'event '
    if ratelist[1] != baserate[0] and ratelist[3] != baserate[0] or ratelist[5] != baserate[0]:
        viewrate[2] = '+ '
    if ratelist[1] != baserate[0] and ratelist[3] != baserate[0] and ratelist[5] != baserate[0]:
        viewrate[2] = '++ '
    if ratelist[7] != baserate[0] or ratelist[9] != baserate[0] or ratelist[11] != baserate[0]:
        viewrate[3] = 'breeding '
    if ratelist[13] != baserate[0] or ratelist[15] != baserate[0] or ratelist[17] != baserate[0]:
        viewrate[0] = 'special '
    # traitement embed
    embedrate = discord.Embed(title="Multiplicateur en Offi",
                              description=f"{''.join(viewrate)}en cours sur le reseau officiel", color=0x00ff00)
    embedrate.add_field(name="Multiplacateur\nApprivoisement", value=ratelist[1], inline=True)
    embedrate.add_field(name="Multiplicateur\nRécolte", value=ratelist[3], inline=True)
    embedrate.add_field(name="Multiplicateur\nXP", value=ratelist[5], inline=True)
    embedrate.add_field(name="Intervale\nAccouplement", value=ratelist[7], inline=True)
    embedrate.add_field(name="Maturation\ndes bébé", value=ratelist[9], inline=True)
    embedrate.add_field(name="Eclosion des\noeufs/Gestation", value=ratelist[11], inline=True)
    embedrate.add_field(name="Intervale\nImprint", value=ratelist[13], inline=True)
    embedrate.add_field(name="Multiplicateur\nde l'Imprint", value=ratelist[15], inline=True)
    embedrate.add_field(name="Multiplicateur\nHexagone", value=ratelist[17], inline=True)
    print('rate asked')
    await ctx.channel.send(embed=embedrate)


# -----tribe bot--------------------------------------------------------------------------------------------------------
# invite
@bot.command()
@trib_core()
async def invite(ctx):
    link = await ctx.channel.create_invite(max_age=21600, max_uses=1)
    await ctx.send(link)


# Ban check
@bot.command()
@trib_chan()
async def ban(ctx, idrq):
    bandb = datban.splitlines()
    for idban in bandb:
        print(idban)
        if int(idrq) == int(idban):
            await ctx.send(":white_check_mark: this SteamID is globally banned from the official server network")
            return
    await ctx.send("this SteamID is not banned from the official server network")

@bot.command()
@trib_chan()
# 00d00h00m00s
async def rappel(ctx, time, *object):
    stime = ""
    timeview = ['', '', '', '']
    try:
        timea = time.removesuffix('s').rpartition('m')
        timewithsec = int(timea[2])
        timeview[3] = f"{timea[2]}seconds"
        print(f"{timea[2]}seconds")
        try:
            timeb = timea[0].rpartition('h')
            timewithmin = int(timewithsec) + int(int(timeb[2])*60)
            timeview[2] = f"{timeb[2]}minutes"
            try:
                timec = timeb[0].rpartition('d')
                stime = int(timewithmin) + int(int(timec[2])*3600) + int(int(timec[0]) * 86400)
                timeview[0] = f"{timec[0]}jours"
                timeview[1] = f"{timec[2]}heures"
            except:
                timeb = timea[0].rpartition('h')
                stime = int(timewithmin) + int(int(timeb[0]) * 3600)
                timeview[1] = f"{timeb[0]}heures"
        except:
            timea = time.removesuffix('s').rpartition('m')
            stime = int(timewithsec) + int(int(timea[0])*60)
            timeview[2] = f"{timea[0]}minutes"
            print(f"{timea[0]}minutes")
    except:
        await ctx.send("merci d'envoyer un temps correct 00d00h00m00s")
    print(timeview)
    print(stime)
    await ctx.send(f"{ctx.author.mention}\nun rappel sera envoyer dans{' '.join(timeview)} pour {object}")
    await asyncio.sleep(stime)
    await ctx.send(f"{ctx.author.mention}\nrappel pour {object}")


# -----Member DataBase-------------------
# DB member
@bot.command()
@trib_admin()
async def members(ctx, joueur):
    c_kunu = connection.cursor()
    dbkunurq = c_kunu.execute('SELECT * FROM kunu_membre')
    for dat in dbkunurq.fetchall():
        if str.lower(joueur) in str.lower(dat[2]) or str.lower(joueur) in str.lower(dat[7]):
            embedmember = discord.Embed(title=dat[2], description=f"empty")
            if dat[3] is not None:
                embedmember.add_field(name="Steam Id", value=dat[3], inline=True)
            if dat[4] is not None:
                embedmember.add_field(name="Steam name", value=dat[4], inline=True)
            if dat[5] is not None:
                embedmember.add_field(name="Epic Id", value=dat[5], inline=True)
            if dat[6] is not None:
                embedmember.add_field(name="Epic name", value=dat[6], inline=True)
            if dat[7] is not None:
                embedmember.add_field(name="Nom d'avatar", value=dat[7], inline=True)
            if dat[8] is not None:
                embedmember.add_field(name="code pin", value=dat[8], inline=True)
            await ctx.channel.send(embed=embedmember)
    await ctx.send('done')
    c_kunu.close()


# -----BP--------------------------------------------------------------
# list
@bot.command()
@trib_chan()
async def bp_list(ctx):
    typebp = []
    for typebpdb in bpdatlist:
        typebp.append(typebpdb[3])
    # traitement embed
    embedlist = discord.Embed(title=f"Recorded BluePrint's List",
                            description="Make \"!bp <type bp>\" request for show BP's")
    embedlist.add_field(name='type bp', value="\n".join(typebp), inline=False)
    await ctx.channel.send(embed=embedlist)
    print('bp list asked')


# request bp
@bot.command()
@trib_chan()
async def bp(ctx, bparg):
    print(bparg)
    if str.lower(bparg) == "flak":
        # traitement embed
        embedflakselect = discord.Embed(title=f"Flak armor",
                                  description="Select flak armor piece")
        embedflakselect.add_field(name='flak piece', value="1️⃣ -> helmet\n2️⃣ -> chestpiece\n3️⃣ -> leggins\n4️⃣ -> Boots\n5️⃣ -> Gauntlets", inline=False)
        flakpiecselect = await ctx.channel.send(embed=embedflakselect)
        await flakpiecselect.add_reaction("1️⃣")
        await flakpiecselect.add_reaction("2️⃣")
        await flakpiecselect.add_reaction("3️⃣")
        await flakpiecselect.add_reaction("4️⃣")
        await flakpiecselect.add_reaction("5️⃣")

        def checkbpaddreact(reactionflak, user):
            return user == ctx.message.author and flakpiecselect.id == reactionflak.message.id and (
                        str(reactionflak.emoji) == "1️⃣" or str(reactionflak.emoji) == "2️⃣" or str(
                    reactionflak.emoji) == "3️⃣" or str(reactionflak.emoji) == "4️⃣" or str(reactionflak.emoji) == "5️⃣")

        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=15, check=checkbpaddreact)
            if reaction.emoji == "1️⃣":
                bparg = "flak_h"
            if reaction.emoji == "2️⃣":
                bparg = "flak_c"
            if reaction.emoji == "3️⃣":
                bparg = "flak_l"
            if reaction.emoji == "4️⃣":
                bparg = "flak_b"
            if reaction.emoji == "5️⃣":
                bparg = "flak_g"
        except:
            await ctx.send("select bp cancelled")
            return

    color = ""
    for bpdat in bpdatlist:
        if str.lower(bparg) == str(bpdat[2]) or str.lower(bparg) == str(bpdat[3]) or str.lower(bparg) == str(
                bpdat[4]):
            c_bp = connection.cursor()
            bp_reslt = (bpdat[2],)
            rq_bp = c_bp.execute(f'SELECT * FROM bp_db WHERE type_bp = ? ORDER BY arm_dmg DESC', bp_reslt)
            for row in rq_bp.fetchall():
                print(row[0], row[1], row[2], row[3], row[4])
                # couleur
                if row[2] == prim[1]:
                    color = prim[0]
                if row[2] == ram[1]:
                    color = ram[0]
                if row[2] == app[1]:
                    color = app[0]
                if row[2] == jour[1]:
                    color = jour[0]
                if row[2] == mast[1]:
                    color = mast[0]
                if row[2] == asc[1]:
                    color = asc[0]
                # ressource
                rscview1 = [bpdat[6]]
                rscview2 = [row[5]]
                rscview3 = [str(int(int(row[5]) / int(row[3])))]
                if row[6] is not None:
                    rscview1.append(bpdat[7])
                    rscview2.append(row[6])
                    rscview3.append(str(int(int(row[6]) / int(row[3]))))
                if row[7] is not None:
                    rscview1.append(bpdat[8])
                    rscview2.append(row[7])
                    rscview3.append(str(int(int(row[7]) / int(row[3]))))
                if row[8] is not None:
                    rscview1.append(bpdat[9])
                    rscview2.append(row[8])
                    rscview3.append(str(int(int(row[8]) / int(row[3]))))
                if row[9] is not None:
                    rscview1.append(bpdat[10])
                    rscview2.append(row[9])
                    rscview3.append(str(int(int(row[9]) / int(row[3]))))
                if row[10] is not None:
                    rscview1.append(bpdat[11])
                    rscview2.append(row[10])
                    rscview3.append(str(int(int(row[10]) / int(row[3]))))
                if row[11] is not None:
                    rscview1.append(bpdat[12])
                    rscview2.append(row[11])
                    rscview3.append(str(int(int(row[11]) / int(row[3]))))
                if row[12] is not None:
                    rscview1.append(bpdat[13])
                    rscview2.append(row[12])
                    rscview3.append(str(int(int(row[12]) / int(row[3]))))
                # type bp
                titlebp = ''
                descbp = ''
                if bpdat[1] == 0:
                    titlebp = f'{bpdat[2].capitalize()} Saddle'
                    descbp = f'{row[2].capitalize()} {row[1].capitalize()} Saddle with {row[3]}% armor'
                if bpdat[1] == 1:
                    titlebp = f'{bpdat[3].capitalize()}'
                    descbp = f'{row[2].capitalize()} {bpdat[3].capitalize()} with {row[3]}% armor and {row[4]} durability'
                if bpdat[1] == 2:
                    titlebp = f'{bpdat[3].capitalize()}'
                    descbp = f'{row[2].capitalize()} {bpdat[3].capitalize()} with {row[3]}% damage and {row[4]} durability'
                # traitement embed
                embedbp = discord.Embed(title=f"BP {row[0]} - {titlebp}",
                                        description=descbp, color=color)
                embedbp.set_thumbnail(url=bpdat[5])
                embedbp.add_field(name="Ingredients", value='\n'.join(rscview1).title(), inline=True)
                embedbp.add_field(name="Quantity", value='\n'.join(rscview2), inline=True)
                if bpdat[1] == 0:
                    embedbp.add_field(name="Ratio", value='\n'.join(rscview3), inline=True)
                if bpdat[1] == 1:
                    embedbp.add_field(name=bpdat[14], value=row[13], inline=False)
                    embedbp.add_field(name=bpdat[15], value=row[14], inline=True)
                await ctx.channel.send(embed=embedbp)
            c_bp.close()
            await ctx.send(":white_check_mark: **done**")
            print(f'bp {bparg} asked')
            return
    else:
        await ctx.send("bp not found")
        print(f'bp {bparg[0]} dont found')


# craft saddle
@bot.command()
@trib_chan()
async def bp_craft(ctx, bpid, quant):
    color = ""
    c_craft = connection.cursor()
    craft_reslt = (f'{str.lower(bpid)}',)
    rq_craft = c_craft.execute('SELECT * FROM bp_db WHERE id_bp = ?', craft_reslt)
    for row in rq_craft.fetchall():
        # couleur
        if row[2] == prim[1]:
            color = prim[0]
        if row[2] == ram[1]:
            color = ram[0]
        if row[2] == app[1]:
            color = app[0]
        if row[2] == jour[1]:
            color = jour[0]
        if row[2] == mast[1]:
            color = mast[0]
        if row[2] == asc[1]:
            color = asc[0]
        # ressource
        rsc1 = row[5].rsplit(':')
        rscview1 = [rsc1[0]]
        rscview2 = [rsc1[1]]
        rscview3 = [str(int(rsc1[1]) * int(quant))]
        if row[6] is not None:
            rsc2 = row[6].rsplit(':')
            rscview1.append(rsc2[0])
            rscview2.append(rsc2[1])
            rscview3.append(str(int(rsc2[1]) * int(quant)))
        if row[7] != None:
            rsc3 = row[7].rsplit(':')
            rscview1.append(rsc3[0])
            rscview2.append(rsc3[1])
            rscview3.append(str(int(rsc3[1]) * int(quant)))
        if row[8] != None:
            rsc4 = row[8].rsplit(':')
            rscview1.append(rsc4[0])
            rscview2.append(rsc4[1])
            rscview3.append(str(int(rsc4[1]) * int(quant)))
        if row[9] != None:
            rsc5 = row[9].rsplit(':')
            rscview1.append(rsc5[0])
            rscview2.append(rsc5[1])
            rscview3.append(str(int(rsc5[1]) * int(quant)))
        if row[10] != None:
            rsc6 = row[10].rsplit(':')
            rscview1.append(rsc6[0])
            rscview2.append(rsc6[1])
            rscview3.append(str(int(rsc6[1]) * int(quant)))
        # traitement embed
        embedbp = discord.Embed(title=f"for craft {quant} {row[1]} saddle (BP {row[0]})",
                                description=f"{row[2]} saddle with {row[3]}% dmg", color=color)
        embedbp.add_field(name="Ingredients",
                          value='\n'.join(rscview1), inline=True)
        embedbp.add_field(name="Quantity by 1",
                          value='\n'.join(rscview2), inline=True)
        embedbp.add_field(name=f"Quantity by {quant}",
                          value='\n'.join(rscview3), inline=True)
        await ctx.channel.send(embed=embedbp)
    c_craft.close()
    print('craft bp asked')


@bot.command()
@trib_admin()
async def bp_add(ctx):
    # mise en place requete
    idbpadd = ""
    datbpadd = []
    typelist = []
    color = ""
    for typebpdb in bpdatlist:
        datbpadd.append(typebpdb)
        typelist.append(typebpdb[2])
    # embed selection type bp
    embedlist = discord.Embed(title=f"Add BP",
                            description="Please, enter type BP you want add")
    embedlist.add_field(name='type bp', value="\n".join(typelist), inline=False)
    await ctx.channel.send(embed=embedlist)

    def checkbpaddtxt(message):
        return message.author == ctx.message.author and message.channel == ctx.message.channel

    typebpadd = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
    # création bp
    try:
        for rowbpdat in datbpadd:
            if str(typebpadd.content) == str(rowbpdat[2]):
                print(rowbpdat[2])
                datbpadd = rowbpdat
                c_addbp = connection.cursor()
                bpadded = (c_addbp.lastrowid, f'{typebpadd.content}')
                c_addbp.execute('INSERT INTO bp_db (id_bp,type_bp) VALUES (?,?)', bpadded)
                idbpadd = c_addbp.lastrowid
                connection.commit()
                c_addbp.close()
    except:
        await ctx.send("BP type don't found")

        return
    # embed selection qualité
    embedlist = discord.Embed(title=f"Add BP",
                            description="Please, react with good emoji for select quality")
    embedlist.add_field(name='Quality BP', value="1️⃣ -> Primitive\n2️⃣ -> Ramshackle\n3️⃣ -> Apprentice\n4️⃣ -> Journeyman\n5️⃣ -> Mastercraft\n6️⃣ -> Ascendant", inline=False)
    qualselect = await ctx.channel.send(embed=embedlist)
    await qualselect.add_reaction("1️⃣")
    await qualselect.add_reaction("2️⃣")
    await qualselect.add_reaction("3️⃣")
    await qualselect.add_reaction("4️⃣")
    await qualselect.add_reaction("5️⃣")
    await qualselect.add_reaction("6️⃣")

    # ajout qualité
    def checkbpaddreact(reaction, user):
        return user == ctx.message.author and qualselect.id == reaction.message.id and (str(reaction.emoji) == "1️⃣" or str(reaction.emoji) == "2️⃣" or str(reaction.emoji) == "3️⃣" or str(reaction.emoji) == "4️⃣" or str(reaction.emoji) == "5️⃣" or str(reaction.emoji) == "6️⃣")
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=15, check=checkbpaddreact)
        if reaction.emoji == "1️⃣":
            qualadd = ("primitive", f"{idbpadd}")
            c_addbp = connection.cursor()
            c_addbp.execute('UPDATE bp_db SET rarity = ? WHERE id_bp = ?', qualadd)
            connection.commit()
            c_addbp.close()
        if reaction.emoji == "2️⃣":
            qualadd = ("ramshackle", f"{idbpadd}")
            c_addbp = connection.cursor()
            c_addbp.execute('UPDATE bp_db SET rarity = ? WHERE id_bp = ?', qualadd)
            connection.commit()
            c_addbp.close()
        if reaction.emoji == "3️⃣":
            qualadd = ("apprentice", f"{idbpadd}")
            c_addbp = connection.cursor()
            c_addbp.execute('UPDATE bp_db SET rarity = ? WHERE id_bp = ?', qualadd)
            connection.commit()
            c_addbp.close()
        if reaction.emoji == "4️⃣":
            qualadd = ("journeyman", f"{idbpadd}")
            c_addbp = connection.cursor()
            c_addbp.execute('UPDATE bp_db SET rarity = ? WHERE id_bp = ?', qualadd)
            connection.commit()
            c_addbp.close()
        if reaction.emoji == "5️⃣":
            qualadd = ("mastercraft", f"{idbpadd}")
            c_addbp = connection.cursor()
            c_addbp.execute('UPDATE bp_db SET rarity = ? WHERE id_bp = ?', qualadd)
            connection.commit()
            c_addbp.close()
        if reaction.emoji == "6️⃣":
            qualadd = ("ascendant", f"{idbpadd}")
            c_addbp = connection.cursor()
            c_addbp.execute('UPDATE bp_db SET rarity = ? WHERE id_bp = ?', qualadd)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    #ajout armure/domage
    try:
        if datbpadd[1] == 0:
            await ctx.send("Please enter Saddle armor")
        if datbpadd[1] == 1:
            await ctx.send("Please enter Armor rating")
        """other command
        """
        armdmgadd = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
        c_addbp = connection.cursor()
        ardmadd = (armdmgadd.content, f'{idbpadd}')
        c_addbp.execute('UPDATE bp_db SET arm_dmg = ? WHERE id_bp = ?', ardmadd)
        connection.commit()
        c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    #ajout dura
    try:
        if datbpadd[1] == 1:
            await ctx.send("Please enter Durability")
            armdmgadd = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            ardmadd = (armdmgadd.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET dura = ? WHERE id_bp = ?', ardmadd)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    # ajout ressources
    try:
        if datbpadd[6] is not None:
            await ctx.send(f"Please enter {datbpadd[6]} quantity")
            rsc1add = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            rsc1 = (rsc1add.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET rsc1 = ? WHERE id_bp = ?', rsc1)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    try:
        if datbpadd[7] is not None:
            await ctx.send(f"Please enter {datbpadd[7]} quantity")
            rsc2add = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            rsc2 = (rsc2add.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET rsc2 = ? WHERE id_bp = ?', rsc2)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    try:
        if datbpadd[8] is not None:
            await ctx.send(f"Please enter {datbpadd[8]} quantity")
            rsc3add = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            rsc3 = (rsc3add.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET rsc3 = ? WHERE id_bp = ?', rsc3)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    try:
        if datbpadd[9] is not None:
            await ctx.send(f"Please enter {datbpadd[9]} quantity")
            rsc4add = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            rsc4 = (rsc4add.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET rsc4 = ? WHERE id_bp = ?', rsc4)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    try:
        if datbpadd[10] is not None:
            await ctx.send(f"Please enter {datbpadd[10]} quantity")
            rsc5add = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            rsc5 = (rsc5add.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET rsc5 = ? WHERE id_bp = ?', rsc5)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    try:
        if datbpadd[11] is not None:
            await ctx.send(f"Please enter {datbpadd[11]} quantity")
            rsc6add = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            rsc6 = (rsc6add.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET rsc6 = ? WHERE id_bp = ?', rsc6)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    try:
        if datbpadd[12] is not None:
            await ctx.send(f"Please enter {datbpadd[12]} quantity")
            rsc7add = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            rsc7 = (rsc7add.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET rsc7 = ? WHERE id_bp = ?', rsc7)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    try:
        if datbpadd[13] is not None:
            await ctx.send(f"Please enter {datbpadd[13]} quantity")
            rsc8add = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            rsc8 = (rsc8add.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET rsc8 = ? WHERE id_bp = ?', rsc8)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    # ajout data
    try:
        if datbpadd[14] is not None:
            await ctx.send(f"Please enter {datbpadd[14]} quantity")
            dat1add = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            dat1 = (dat1add.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET dat1 = ? WHERE id_bp = ?', dat1)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    try:
        if datbpadd[15] is not None:
            await ctx.send(f"Please enter {datbpadd[15]} quantity")
            dat2add = await bot.wait_for("message", timeout=20, check=checkbpaddtxt)
            c_addbp = connection.cursor()
            dat2 = (dat2add.content, f'{idbpadd}')
            c_addbp.execute('UPDATE bp_db SET dat2 = ? WHERE id_bp = ?', dat2)
            connection.commit()
            c_addbp.close()
    except:
        await ctx.send("adding cancelled")
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
    await ctx.send("you want add this bp ?")
    c_bp = connection.cursor()
    bpadd = (f'{idbpadd}',)
    rq_bp = c_bp.execute(f'SELECT * FROM bp_db WHERE id_bp = ? ', bpadd)
    for row in rq_bp.fetchall():
        # couleur
        if row[2] == prim[1]:
            color = prim[0]
        if row[2] == ram[1]:
            color = ram[0]
        if row[2] == app[1]:
            color = app[0]
        if row[2] == jour[1]:
            color = jour[0]
        if row[2] == mast[1]:
            color = mast[0]
        if row[2] == asc[1]:
            color = asc[0]
        # ressource
        rscview1 = [datbpadd[6]]
        rscview2 = [row[5]]
        rscview3 = [str(int(int(row[5]) / int(row[3])))]
        if row[6] is not None:
            rscview1.append(datbpadd[7])
            rscview2.append(row[6])
            rscview3.append(str(int(int(row[6]) / int(row[3]))))
        if row[7] is not None:
            rscview1.append(datbpadd[8])
            rscview2.append(row[7])
            rscview3.append(str(int(int(row[7]) / int(row[3]))))
        if row[8] is not None:
            rscview1.append(datbpadd[9])
            rscview2.append(row[8])
            rscview3.append(str(int(int(row[8]) / int(row[3]))))
        if row[9] is not None:
            rscview1.append(datbpadd[10])
            rscview2.append(row[9])
            rscview3.append(str(int(int(row[9]) / int(row[3]))))
        if row[10] is not None:
            rscview1.append(datbpadd[11])
            rscview2.append(row[10])
            rscview3.append(str(int(int(row[10]) / int(row[3]))))
        # type bp
        titlebp = ''
        descbp = ''
        if datbpadd[1] == 0:
            titlebp = f'{datbpadd[2].capitalize()} Saddle'
            descbp = f'{row[2].capitalize()} {row[1].capitalize()} Saddle with {row[3]}% armor'
        if datbpadd[1] == 1:
            titlebp = f'{datbpadd[3].capitalize()}'
            descbp = f'{row[2].capitalize()} {datbpadd[3].capitalize()} with {row[3]}% armor and {row[4]} durability'
        if datbpadd[1] == 2:
            titlebp = f'{datbpadd[3].capitalize()}'
            descbp = f'{row[2].capitalize()} {datbpadd[3].capitalize()} with {row[3]}% damage and {row[4]} durability'
        # traitement embed
        embedbp = discord.Embed(title=f"BP {row[0]} - {titlebp}",
                                description=descbp, color=color)
        embedbp.set_thumbnail(url=datbpadd[5])
        embedbp.add_field(name="Ingredients", value='\n'.join(rscview1).title(), inline=True)
        embedbp.add_field(name="Quantity", value='\n'.join(rscview2), inline=True)
        if datbpadd[1] == 0:
            embedbp.add_field(name="Ratio", value='\n'.join(rscview3), inline=True)
        if datbpadd[1] == 1:
            embedbp.add_field(name=datbpadd[14], value=row[13], inline=False)
            embedbp.add_field(name=datbpadd[15], value=row[14], inline=True)
        showbpid = await ctx.channel.send(embed=embedbp)
        await showbpid.add_reaction("👍")
        await showbpid.add_reaction("👎")
    c_bp.close()

    # ajout qualité
    def checkbpaddreact(reaction, user):
        return user == ctx.message.author and showbpid.id == reaction.message.id and (
                str(reaction.emoji) == "👍" or str(reaction.emoji) == "👎")
    reaction, user = await bot.wait_for("reaction_add", timeout=15, check=checkbpaddreact)
    if reaction.emoji == "👍":
        await ctx.send("BP added success")
    if reaction.emoji == "👎":
        delreqadd = (f"{idbpadd}",)
        c_delreq = connection.cursor()
        c_delreq.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreqadd)
        connection.commit()
        c_delreq.close()
        await ctx.send("adding cancelled")


@bot.command()
@trib_admin()
async def bp_del(ctx, del_id):
    color = ""
    infobp = []
    delreq = (f"{del_id}",)
    c_delbpview = connection.cursor()
    c_delbpview.execute(f'SELECT * FROM bp_db WHERE id_bp = ?', delreq)
    for row in c_delbpview.fetchall():
        for bpdat in bpdatlist:
            if row[1] == bpdat[2]:
                infobp = (bpdat[1], bpdat[2], bpdat[3], bpdat[5])
        # couleur
        if row[2] == prim[1]:
            color = prim[0]
        if row[2] == ram[1]:
            color = ram[0]
        if row[2] == app[1]:
            color = app[0]
        if row[2] == jour[1]:
            color = jour[0]
        if row[2] == mast[1]:
            color = mast[0]
        if row[2] == asc[1]:
            color = asc[0]
        # ressource
        rsc1 = row[5].rsplit(':')
        rscview1 = [rsc1[0]]
        rscview2 = [rsc1[1]]
        rscview3 = [str(int(int(rsc1[1]) / int(row[3])))]
        if row[6] is not None:
            rsc2 = row[6].rsplit(':')
            rscview1.append(rsc2[0])
            rscview2.append(rsc2[1])
            rscview3.append(str(int(int(rsc2[1]) / int(row[3]))))
        if row[7] is not None:
            rsc3 = row[7].rsplit(':')
            rscview1.append(rsc3[0])
            rscview2.append(rsc3[1])
            rscview3.append(str(int(int(rsc3[1]) / int(row[3]))))
        if row[8] is not None:
            rsc4 = row[8].rsplit(':')
            rscview1.append(rsc4[0])
            rscview2.append(rsc4[1])
            rscview3.append(str(int(int(rsc4[1]) / int(row[3]))))
        if row[9] is not None:
            rsc5 = row[9].rsplit(':')
            rscview1.append(rsc5[0])
            rscview2.append(rsc5[1])
            rscview3.append(str(int(int(rsc5[1]) / int(row[3]))))
        if row[10] is not None:
            rsc6 = row[10].rsplit(':')
            rscview1.append(rsc6[0])
            rscview2.append(rsc6[1])
            rscview3.append(str(int(int(rsc6[1]) / int(row[3]))))
        await ctx.send(f"you want delete this bp")
        # type bp
        titlebp = ''
        descbp = ''
        if infobp[0] == 0:
            titlebp = f'{infobp[1].capitalize()} Saddle'
            descbp = f'{row[2].capitalize()} {row[1].capitalize()} Saddle with {row[3]}% armor'
        if infobp[0] == 1:
            titlebp = f'{infobp[1].capitalize()}'
            descbp = f'{row[2].capitalize()} {infobp[2].capitalize()} with {row[3]}% armor and {row[4]} durability'
        if infobp[0] == 2:
            titlebp = f'{infobp[1].capitalize()}'
            descbp = f'{row[2].capitalize()} {infobp[2].capitalize()} with {row[3]}% damage and {row[4]} durability'
            # traitement embed
        embedbp = discord.Embed(title=f"BP {row[0]} - {titlebp}",
                                    description=descbp, color=color)
        embedbp.set_thumbnail(url=infobp[3])
        embedbp.add_field(name="Ingredients", value='\n'.join(rscview1).title(), inline=True)
        embedbp.add_field(name="Quantity", value='\n'.join(rscview2), inline=True)
        validcheck = await ctx.channel.send(embed=embedbp)
        await validcheck.add_reaction("👍")
        await validcheck.add_reaction("👎")
        await validcheck.add_reaction("⏱")

        def checkEmoji(reaction, user):
            return ctx.message.author == user and validcheck.id == reaction.message.id and ((str(reaction.emoji) == "👍") or (str(reaction.emoji) == "👎"))

        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=15, check=checkEmoji)
            if reaction.emoji == "👍":
                c_delbpview.close()
                c_delbp = connection.cursor()
                c_delbp.execute(f'DELETE FROM bp_db WHERE id_bp = ?', delreq)
                connection.commit()
                c_delbp.close()
                await ctx.send(f"{del_id} deleted successfully")
            if reaction.emoji == "👎":
                await validcheck.clear_reaction("⏱")
                await ctx.send(f"delete bp canceled")
                return
        except:
            await validcheck.clear_reaction("⏱")
            await ctx.send(f"delete bp canceled")


# -----token--------------------------------------------------------
ask = ("token",)
c_tok = connection.cursor()
c_tok.execute('SELECT * FROM data WHERE type = ?', ask)
token = c_tok.fetchone()
bot.run(token[2])
connection.close()
