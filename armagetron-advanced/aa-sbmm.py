import discord
import re
import random
from datetime import datetime, timedelta
import statistics

#client = discord.Client()

intents = discord.Intents.all()
client = discord.Client(intents=intents)

################ TIER DECLARATIONS #################
######## Tiers Withheld from Public Posting ########

tierS = []

tierA = []

tierB = []

tierC = []

tierD = []

tierE = []

tierF = []

trustees = [397820413545152524,838470464246251540,198089380714381312,361681542399000577,136790348289671168,
            271383985232412672,133766628524425216,822209993750478929]

####################################################

everyone = tierS + tierA + tierB + tierC + tierD + tierE + tierF
    
####################################################


lobby = []
sequence = 1
teamgold = []
teamblue = []
is11 = False
lobby_balance = 0
lobby_grade = 'z'
all_members = []
fort11time = datetime(2000,1,1)
time = datetime(2000,1,1)
fort11msg_sent = False
over_msg_count = 0
queue_start = datetime(2000,1,1)
queue_end = datetime(2000,1,1)
queue_time = datetime(2000,1,1)
rolling = False
lobby_parity = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global trustees
    global is11
    global sequence
    global teamblue
    global teamgold
    global lobby_balance
    global lobby_grade
    global all_members
    global fort11time
    global time
    global fort11msg_sent
    global over_msg_count
    global queue_start
    global queue_end
    global queue_time
    global rolling
    global lobby_parity

    now = datetime.now()
    
    if message.author == client.user:
        return
    if message.channel.name != 'pickup':
        return

    if (message.author.id == 818329943003365397 or message.author.id == 397820413545152524) and message.content.startswith('----- Fortress ready to start! -----'):
        sequence = 1
        lobby.clear()
        teamblue.clear()
        teamgold.clear()

        queue_end = datetime.now()
        queue_time = queue_end - queue_start
        
        msg = message.content
        queue = parseQueue(msg)
        for i in range(len(queue)):
            lobby.append(queue[i])

        await message.channel.send('👀 u want teams?')
        queue.clear()
        sequence += 1
        is11 = False
        fort11msg_sent = False

    if message.content.startswith('!roll') and sequence == 2 and rolling == False:

        rolling = True
        team_b, team_g = make_teams(lobby)

        guild = await client.fetch_guild(209759416604426242)
        
        captain1 = await guild.fetch_member(get_captain(team_b))
        captain2 = await guild.fetch_member(get_captain(team_g))
        captain1 = captain1.display_name
        captain2 = captain2.display_name

        
        for i in range(len(team_b)):
            user = await client.fetch_user(team_b[i])
            member = await guild.fetch_member(team_b[i])
            teamblue.append(member.display_name)

        for i in range(len(team_g)):
            user = await client.fetch_user(team_g[i])
            member = await guild.fetch_member(team_g[i])
            teamgold.append(member.display_name)

        random.shuffle(teamblue)
        random.shuffle(teamgold)

        lobby_balance = get_balance(get_score(team_b),get_score(team_g),lobby)
        lobby_grade = get_grade(get_score(team_b),get_score(team_g))
        lobby_parity = get_parity(lobby)

        
        team_b.clear()
        team_g.clear()
        
        await message.channel.send(f'```Team Blue: {", ".join(str(x) for x in teamblue)}\nTeam Gold: {", ".join(str(x) for x in teamgold)}```'
                                   f'Captains: {captain1}, {captain2}')
        rolling = False
        teamblue.clear()
        teamgold.clear()

        sequence += 1


        all_members.clear()

        guild = client.get_guild(209759416604426242)

        #guild = client.get_guild(991114151336362085)
        
        for member in guild.members:
            all_members.append(str(member.id))


    if message.content.startswith('!clear') and sequence >= 2 and message.author.id in trustees:
        await message.channel.send('queues cleared.')
        teamblue.clear()
        teamgold.clear()
        lobby.clear()
        sequence = 1
        

    if message.content.startswith('!reroll') and sequence >= 3 and message.author.id in trustees and rolling == False:
        rolling = True
        team_b, team_g = make_teams(lobby)

        teamblue.clear()
        teamgold.clear()
        
        guild = await client.fetch_guild(209759416604426242)
        
        captain1 = await guild.fetch_member(get_captain(team_b))
        captain2 = await guild.fetch_member(get_captain(team_g))
        captain1 = captain1.display_name
        captain2 = captain2.display_name

        
        for i in range(len(team_b)):
            user = await client.fetch_user(team_b[i])
            member = await guild.fetch_member(team_b[i])
            teamblue.append(member.display_name)

        for i in range(len(team_g)):
            user = await client.fetch_user(team_g[i])
            member = await guild.fetch_member(team_g[i])
            teamgold.append(member.display_name)

        random.shuffle(teamblue)
        random.shuffle(teamgold)

        lobby_balance = get_balance(get_score(team_b),get_score(team_g),lobby)
        lobby_grade = get_grade(get_score(team_b),get_score(team_g))
        await message.channel.send(f'```Team Blue: {", ".join(str(x) for x in teamblue)}\nTeam Gold: {", ".join(str(x) for x in teamgold)}```'
                                   f'Captains: {captain1}, {captain2}')
        
        sequence += 1
        rolling = False
        
        teamblue.clear()
        teamgold.clear()

    if message.content.startswith('!stats') and message.author.id in trustees:
        
        hours, minutes, seconds = parseTime(queue_time)
        
        await message.channel.send(f':scales: Balance Confidence: {lobby_balance}% \n'
                                   f':trophy: Match Quality: {lobby_grade}\n'
                                   f':bar_chart: Parity: {lobby_parity}\n'
                                   f':stopwatch: Queue Time: {hours} hours, {minutes} minutes, {seconds} seconds')
        
    if message.content.startswith('!sub') and sequence >= 2 and message.author.id in trustees:
        msg = message.content
        out_player, in_player = parseSub(msg)
        guild = await client.fetch_guild(209759416604426242)
   
        if out_player in lobby:
            if in_player in all_members:
                lobby.remove(out_player)
                lobby.append(in_player)
                
                subbed_out = await guild.fetch_member(out_player)
                subbed_in = await guild.fetch_member(in_player)
                subbed_out = subbed_out.display_name
                subbed_in = subbed_in.display_name
                await message.channel.send(f'substituting: **{subbed_out}** for **{subbed_in}**')

                team_b, team_g = make_teams(lobby)

                captain1 = await guild.fetch_member(get_captain(team_b))
                captain2 = await guild.fetch_member(get_captain(team_g))
                captain1 = captain1.display_name
                captain2 = captain2.display_name

                
                for i in range(len(team_b)):
                    user = await client.fetch_user(team_b[i])
                    member = await guild.fetch_member(team_b[i])
                    teamblue.append(member.display_name)

                for i in range(len(team_g)):
                    user = await client.fetch_user(team_g[i])
                    member = await guild.fetch_member(team_g[i])
                    teamgold.append(member.display_name)

                random.shuffle(teamblue)
                random.shuffle(teamgold)

                lobby_balance = get_balance(get_score(team_b),get_score(team_g),lobby)
                lobby_grade = get_grade(get_score(team_b),get_score(team_g))
                lobby_parity = get_parity(lobby)
                
                await message.channel.send(f'⚠️NEW TEAMS:⚠️\n```Team Blue: {", ".join(str(x) for x in teamblue)}\nTeam Gold: {", ".join(str(x) for x in teamgold)}```'
                                           f'Captains: {captain1}, {captain2}')
                teamblue.clear()
                teamgold.clear()
                team_b.clear()
                team_g.clear()
            else:
                await message.channel.send('*IN_PLAYER* was not found in this discord server.')
        else:
            await message.channel.send('*OUT_PLAYER* not found in this lobby.')


    if message.content.startswith('!set') and message.author.id == 397820413545152524:
        msg = message.content
        player, tier = parseSet(msg)
        set_tier(player, tier)
        player = str(await client.fetch_user(player))
        player = player[:-5]
        await message.channel.send(f"{player}'s database entry has been updated.")

    if message.content.startswith('!version') and message.author.id == 397820413545152524:
        await message.channel.send('version: 1.0.13')

    if message.content.startswith('!fortbothelp'):
        await message.channel.send(f'!roll - only works once, after fort pickup fills.\n'
                                   f'!reroll° - reruns algorithm on teams. effectiveness will vary bases on lobby parity.\n'
                                   f'!clear° - clears all data structures. cannot reroll after this has been done.\n'
                                   f'!stats° - gives statistics on balance confidence, match quality, tier spread, and queue time.\n'
                                   f'!sub <id1> <id2>° - will reroll teams with substituted player. IDs can be found by right clicking a user with Developer Mode on.\n'
                                   f'° - available to kronkleberry, Deso, Colton, delinquent, Wind, Ninja Potato, Nanu. find one of us if you need help.')
        

##############################

        
def parseTime(queue_time):
    parsed_time = re.split(':',str(queue_time))
    hours = parsed_time[0]
    minutes = parsed_time[1]
    seconds = parsed_time[2][:2]

    return hours, minutes, seconds
            
def parseSay(msg):
    parsed_string = re.sub(r'.', '', msg, count = 5)
    return parsed_string


def parseSub(msg):
    input_string = msg.replace('>','')
    parsed_string = re.split(' ',input_string)
    return parsed_string[1:]
     
                                    
def parseQueue(msg):
    input_string = msg.replace('>','')
    parsed_string = re.split('@|,|\n',input_string)
    newqueue = parsed_string[2:26:2]
    return newqueue

def parseSet(msg):
    input_string = msg.replace('>','')
    parsed_string = re.split(' ',input_string)
    player = parsed_string[1]
    tier = parsed_string[2]
    return player, tier
    
def set_tier(player,tier):
    player = str(player)

    if player in tierS:
        tierS.remove(player)
    if player in tierA:
        tierA.remove(player)
    if player in tierB:
        tierB.remove(player)
    if player in tierC:
        tierC.remove(player)
    if player in tierD:
        tierD.remove(player)
    if player in tierE:
        tierE.remove(player)
    if player in tierF:
        tierF.remove(player)
    
    if tier == 's':
        tierS.append(player)
    if tier == 'a':
        tierA.append(player)
    if tier == 'b':
        tierB.append(player)
    if tier == 'c':
        tierC.append(player)
    if tier == 'd':
        tierD.append(player)
    if tier == 'e':
        tierE.append(player)
    if tier == 'f':
        tierF.append(player)
    return player, tier
    

def get_captain(team):
    captain = ''
    random.shuffle(team)
    for i in team:
        if captain == '' and (i in tierS or i in tierA or i in tierB or i in tierC):
            captain = i
    return captain

def get_score_player(player):
    score = 0 
    if player in tierS:
       score += 7
    if player in tierA:
       score += 6
    if player in tierB:
       score += 5
    if player in tierC:
       score += 4
    if player in tierD:
       score += 3
    if player in tierE:
       score += 2
    if player in tierF:
       score += 1
    return score

def get_score(team):
    score = 0
    for i in team:
        if i in tierS:
           score += 7
        if i in tierA:
           score += 6
        if i in tierB:
           score += 5
        if i in tierC:
           score += 4
        if i in tierD:
           score += 3
        if i in tierE:
           score += 2
        if i in tierF:
           score += 1
    return score

def get_balance(bluescore,goldscore,queue):
    balance = 100

    grade = get_grade(bluescore,goldscore)
    sd = get_parity(queue)

    if bluescore == goldscore:
        difference = 2.5
    if abs(bluescore - goldscore) == 1:
        difference = 8
    if abs(bluescore - goldscore) == 2:
        difference = 14
    if abs(bluescore - goldscore) == 3:
        difference = 20
    if abs(bluescore - goldscore) >= 4:
        difference = 40

    grade_coeff = (100 - grade)/100

    balance = (balance - difference - (sd*(3)) - (grade_coeff * 8))
    return round(balance,1)

def get_grade(bluescore,goldscore):
    grade = ((bluescore + goldscore) / 77)
    grade = round((grade * 100),1)
    return grade

def get_parity(queue):
    lobby_tiers = []
    for i in queue:
        lobby_tiers.append(get_score_player(i))
    sd = statistics.pstdev(lobby_tiers)
    return round(sd,2)

def make_teams(queue):
    sorted_queue = []
    for i in queue:
        if i not in everyone:
            tierE.append(i)
        
        if i in tierS:
            sorted_queue.append(i)
    for i in queue:
        if i in tierA:
            sorted_queue.append(i)
    for i in queue:
        if i in tierB:
            sorted_queue.append(i)
    for i in queue:
        if i in tierC:
            sorted_queue.append(i)
    for i in queue:
        if i in tierD:
            sorted_queue.append(i)
    for i in queue:
        if i in tierE:
            sorted_queue.append(i)
    for i in queue:
        if i in tierF:
            sorted_queue.append(i)
    
    middle_index = 4
    tophalf = sorted_queue[:middle_index]
    backhalf = sorted_queue[middle_index:]
    random.shuffle(tophalf)
    new_middle = 2


    team_blue = tophalf[:new_middle]
    team_gold = tophalf[new_middle:]
    
    while abs(get_score(team_blue) - get_score(team_gold)) >= 3:

        team_blue = []
        team_gold = []
        random.shuffle(tophalf)
        new_middle = 2
        team_blue = tophalf[:new_middle]
        team_gold = tophalf[new_middle:]

    while len(backhalf) > 0:
        
        if get_score(team_blue) == get_score(team_gold):
            team_blue.append(backhalf[0])
            team_gold.append(backhalf[1])
            backhalf.pop(0)
            backhalf.pop(0)

        elif get_score(team_blue) > get_score(team_gold):
            team_blue.append(backhalf[-1])
            team_gold.append(backhalf[0])
            backhalf.pop(-1)
            backhalf.pop(0)
            
        elif get_score(team_blue) < get_score(team_gold):
            team_gold.append(backhalf[-1])
            team_blue.append(backhalf[0])
            backhalf.pop(-1)
            backhalf.pop(0)

    return team_gold, team_blue

client.run('')
