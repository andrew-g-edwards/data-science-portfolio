import discord
import re
import random
from datetime import datetime, timedelta
import statistics
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from loguru import logger

#######   Set up logging to file   ########

logger.add("/home/kronk/debug/teamsbot.log", level="DEBUG", rotation="28 days")

DISCORD_BOT_TOKEN = discord_token

############## GOOGLE SHEET API ##################

SHEET_URL = sheet_url


def read_google_sheet(sheet_name: str, json_keyfile: str, worksheet_name: str = 'Sheet1'):
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client_g = gspread.authorize(creds)

    sheet = client_g.open_by_url(SHEET_URL)
    worksheet = sheet.worksheet(worksheet_name)
    return worksheet


def load_tiers(worksheet):
    data = worksheet.get_all_records()

    tier_dict = {'S': set(), 'A': set(), 'B': set(), 'C': set(), 'D': set(), 'E': set(), 'F': set()}

    for row in data:
        player_id = row.get("DiscordId")
        tier = row.get("Tier")

        if player_id and tier in tier_dict:
            tier_dict[tier].add(player_id)

    return tier_dict


worksheet = read_google_sheet(sheet_name="fort_bot_db", json_keyfile="psyched-bonfire-349822-80e79db8825a.json")

tier_dict = load_tiers(worksheet)

for tier, player_ids in tier_dict.items():
    tier_dict[tier] = {str(pid) for pid in player_ids}

everyone = set().union(*tier_dict.values())

###################################################

intents = discord.Intents.all()
client = discord.Client(intents=intents)

########## trustees: kb, wind, ampz, deso, vov, deli, nanu

trustees = [397820413545152524, 838470464246251540, 198089380714381312, 361681542399000577, 136790348289671168,
            271383985232412672, 133766628524425216]

####################################################

SCORE_MAP = {
    'S': 7,
    'A': 6,
    'B': 5,
    'C': 4,
    'D': 3,
    'E': 2,
    'F': 1
}

lobby = []
sequence = 1
teamgold = []
teamblue = []
is11 = False
lobby_balance = 0
lobby_grade = 'z'
all_members = []
fort11time = datetime(2000, 1, 1)
time = datetime(2000, 1, 1)
fort11msg_sent = False
queue_start = datetime(2000, 1, 1)
queue_end = datetime(2000, 1, 1)
queue_time = datetime(2000, 1, 1)
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
    global queue_start
    global queue_end
    global queue_time
    global rolling
    global lobby_parity
    global tier_dict
    global everyone

    now = datetime.now()

    if message.author == client.user:
        return

    if message.guild is None:
        if message.author.id == 397820413545152524:
            if message.content.startswith("!reload"):
                new_worksheet = read_google_sheet(
                    sheet_name="fort_bot_db",
                    json_keyfile="psyched-bonfire-349822-80e79db8825a.json"
                )
                new_tier_dict = load_tiers(new_worksheet)
                tier_dict = new_tier_dict

                for tier, player_ids in tier_dict.items():
                    tier_dict[tier] = {str(pid) for pid in player_ids}
                everyone = set().union(*tier_dict.values())


                await message.channel.send("Tier data reloaded from Google Sheets!")

        return

    if message.channel.name != 'pickup':
        return

    if (
            message.author.id == 818329943003365397 or message.author.id == 397820413545152524) and message.content.startswith(
        '----- Fortress ready to start! -----'):
        logger.debug("New fortress match detected at " + now.strftime("%m/%d/%Y, %H:%M:%S"))
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
        logger.debug("Created a lobby based on the following input: \n\n" + msg + "\n\n with the following queue: \n" + "\n".join(queue) + "\n\n that looks like this: \n" + "\n".join(lobby))

        await message.channel.send('👀 u want teams?')
        queue.clear()
        sequence += 1
        is11 = False
        fort11msg_sent = False

    if message.content.startswith('!roll') and sequence == 2 and rolling == False:

        rolling = True
        team_b, team_g = make_teams(lobby)

        logger.debug("make_teams function called with lobby:\n" + "\n".join(lobby))


        guild = await client.fetch_guild(209759416604426242)

        captain1 = await guild.fetch_member(get_captain(team_b))
        captain2 = await guild.fetch_member(get_captain(team_g))
        captain1 = captain1.display_name
        captain2 = captain2.display_name

        logger.debug("aye aye captains chosen:" + captain1 + "\n" + captain2 + "\n")

        for i in range(len(team_b)):
            user = await client.fetch_user(team_b[i])
            member = await guild.fetch_member(team_b[i])
            teamblue.append(member.display_name)

        for i in range(len(team_g)):
            user = await client.fetch_user(team_g[i])
            member = await guild.fetch_member(team_g[i])
            teamgold.append(member.display_name)

        logger.debug(
                "teams are packed: Team Blue is \n" + ", ".join(teamblue) + "\n Team Gold is \n " + ", ".join(teamgold))

        random.shuffle(teamblue)
        random.shuffle(teamgold)

        logger.debug("team order shuffled")

        lobby_balance = get_balance(team_b, team_g, lobby)
        lobby_grade = get_grade(lobby)
        lobby_parity = get_parity(lobby)

        team_b.clear()
        team_g.clear()

        await message.channel.send(
            f'```Team Blue: {", ".join(str(x) for x in teamblue)}\nTeam Gold: {", ".join(str(x) for x in teamgold)}```'
            f'```Captains: {captain1}, {captain2}```')
        rolling = False

        logger.debug("teams printed to disc")
        teamblue.clear()
        teamgold.clear()

        sequence += 1

        logger.debug("lists cleared, sequence incrimented")

        all_members.clear()

        guild = await client.fetch_guild(209759416604426242)

        for member in guild.members:
            all_members.append(str(member.id))

        logger.debug("created list of @everyone in the discord for potential !subs")

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

        lobby_balance = get_balance(team_b, team_g, lobby)
        lobby_grade = get_grade(lobby)
        await message.channel.send(
            f'```Team Blue: {", ".join(str(x) for x in teamblue)}\nTeam Gold: {", ".join(str(x) for x in teamgold)}```'
            f'```Captains: {captain1}, {captain2}```')

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

        # guild = await client.fetch_guild(209759416604426242)
        guild = await client.fetch_guild(991114151336362085)

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

                lobby_balance = get_balance(team_b, team_g, lobby)
                lobby_grade = get_grade(lobby)
                lobby_parity = get_parity(lobby)

                await message.channel.send(
                    f'⚠️NEW TEAMS:⚠️\n```Team Blue: {", ".join(str(x) for x in teamblue)}\nTeam Gold: {", ".join(str(x) for x in teamgold)}```'
                    f'```Captains: {captain1}, {captain2}```')
                teamblue.clear()
                teamgold.clear()
                team_b.clear()
                team_g.clear()
            else:
                await message.channel.send('*IN_PLAYER* was not found in this discord server.')
        else:
            await message.channel.send('*OUT_PLAYER* not found in this lobby.')

    if message.content.startswith('!version') and message.author.id == 397820413545152524:
        await message.channel.send('version: 1.2.0')

    if message.content.startswith('!fortbothelp'):
        await message.channel.send(f'!roll - only works once, after fort pickup fills.\n'
                                   f'!reroll° - reruns algorithm on teams. effectiveness will vary bases on lobby parity.\n'
                                   f'!clear° - clears all data structures. cannot reroll after this has been done.\n'
                                   f'!stats° - gives statistics on balance confidence, match quality, tier spread, and queue time.\n'
                                   f'!sub <id1> <id2>° - will reroll teams with substituted player. IDs can be found by right clicking a user with Developer Mode on.\n'
                                   f'° - available to kronkleberry, Deso, Colton, delinquent, Wind, Ninja Potato, Nanu. find one of us if you need help.')

    ######### easter eggs ########

    if message.content.startswith('!say') and message.author.id == 397820413545152524:
        msg = message.content
        phrase = parseSay(msg)
        await message.channel.send(phrase)

    if message.author.id == 818329943003365397 or message.author.id == 397820413545152524:
        if 'Fortress (1 / 12)' in message.content:
            queue_start = datetime.now()

        if 'Fortress (11 / 12)' in message.content:
            is11 = True
            fort11msg_sent = False
            fort11time = datetime.now()

        if 'Fortress (10 / 12)' in message.content:
            is11 = False
        if '----- TST ready to start! -----' in message.content and is11 == True:
            await message.channel.send('⚠️ ***FORT CUCK DETECTED*** ⚠️: 8 chimps escaped from the zoo, no one is safe!')

    if now >= fort11time + timedelta(minutes=5) and is11 == True and fort11msg_sent == False:
        fort11msg_sent = True
        await message.channel.send('someone add please 🥺')

    lowercase_msg = message.content.lower()
    if message.author.id == 288920244704247808 and lowercase_msg.startswith('brb'):
        await message.channel.send('sleep tight, wolfie')

    if message.author.id in trustees and (lowercase_msg.startswith('are you here') or lowercase_msg.startswith(
            'is my bot on') or lowercase_msg.startswith('wherefore art thou')):
        await message.channel.send("I'm right here")

    if message.author.id in trustees and (lowercase_msg.startswith('bot on')):
        await message.channel.send("BOT ON")


############################## HELPER FUNCTIONS

def parseTime(queue_time):
    parsed_time = re.split(':', str(queue_time))
    hours = parsed_time[0]
    minutes = parsed_time[1]
    seconds = parsed_time[2][:2]

    return hours, minutes, seconds


def parseSay(msg):
    parsed_string = re.sub(r'.', '', msg, count=5)
    return parsed_string


def parseSub(msg):
    input_string = msg.replace('>', '')
    parsed_string = re.split(' ', input_string)
    return parsed_string[1:]


def parseQueue(msg):
    input_string = msg.replace('>', '')
    parsed_string = re.split('@|,|\n', input_string)
    newqueue = parsed_string[2:26:2]
    return newqueue


def get_captain(team):
    random.shuffle(team)

    for player_id in team:
        player_score = get_score_player(player_id)
        if player_score >= 4:
            return player_id

    return team[0] if team else None


def get_score_player(player_id: str):
    for tier_key, players_set in tier_dict.items():
        if player_id in players_set:
            return SCORE_MAP[tier_key]
    return 0

def get_score(team):
    return sum(get_score_player(player) for player in team)


def get_balance(team_blue, team_gold, queue):
    bluescore = sum(get_score_player(p) for p in team_blue)
    goldscore = sum(get_score_player(p) for p in team_gold)

    lobby_score = bluescore + goldscore
    if lobby_score == 0:
        return 100.0

    diff = abs(bluescore - goldscore)
    base_balance = (1 - (diff / lobby_score)) * 100

    match_grade = get_grade(queue)

    final_confidence = 0.9 * base_balance + 0.1 * match_grade
    return round(final_confidence, 1)


def get_grade(queue):
    total_score = sum(get_score_player(p) for p in queue)

    min_score = 12  # 12 x F-tier (1 point each)
    max_score = 79  # 7 x S-tier (7 points each) + 5 x A-tier (6 points each)

    if total_score <= min_score:
        return 0.0
    if total_score >= max_score:
        return 100.0

    grade = (total_score - min_score) / (max_score - min_score) * 100
    return round(grade, 1)


def get_parity(queue):
    lobby_tiers = []
    for i in queue:
        lobby_tiers.append(get_score_player(i))
    sd = statistics.pstdev(lobby_tiers)
    return round(sd, 2)


def make_teams(queue):
    for player_id in queue:
        if player_id not in everyone:
            tier_dict['E'].add(player_id)

    sorted_queue = []
    tier_order = ['S', 'A', 'B', 'C', 'D', 'E', 'F']

    for tier_key in tier_order:
        for player_id in queue:
            if player_id in tier_dict[tier_key]:
                sorted_queue.append(player_id)

    middle_index = 4
    tophalf = sorted_queue[:middle_index]
    backhalf = sorted_queue[middle_index:]
    random.shuffle(tophalf)
    new_middle = 2

    team_blue = tophalf[:new_middle]
    team_gold = tophalf[new_middle:]

    # Keep re-randomizing if difference in scores is >= 3
    while abs(get_score(team_blue) - get_score(team_gold)) >= 3:
        random.shuffle(tophalf)
        team_blue = tophalf[:new_middle]
        team_gold = tophalf[new_middle:]

    # Then place the rest of the players
    while len(backhalf) >= 2:
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
        else:  # team_blue < team_gold
            team_gold.append(backhalf[-1])
            team_blue.append(backhalf[0])
            backhalf.pop(-1)
            backhalf.pop(0)

    return team_gold, team_blue

client.run(DISCORD_BOT_TOKEN)
