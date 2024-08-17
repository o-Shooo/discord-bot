import discord
from discord.ext import commands
import os
import requests
from dotenv import load_dotenv
from champions import get_champions
import random

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

def fetch_player_id(name, tagLine):
    url = f'https://api.henrikdev.xyz/valorant/v1/account/{name}/{tagLine}'
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Failed to fetch player ID: {r.status_code}")
    data = r.json()
    puuid = data['data']['puuid']
    return puuid

def fetch_match_history(puuid):
    url = f'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/ap/{puuid}?mode=custom&size=1'
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Failed to fetch match history: {r.status_code}")
    d = r.json()
    match_history = d['data'][0]
    return match_history

def dto(data):
    result = []
    players = data['players']['all_players']
    for player in players:
        r = {'name': player["name"], 'score': player["stats"]["score"]}
        result.append(r)
    scores_sorted = sorted(result, key=lambda x: x['score'], reverse=True)
    return scores_sorted

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix="/",
    case_insensitive=True,
    intents=intents
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message: discord.Message):
    content = message.content
    author = message.author
    channel = message.channel

    if author.bot:
        return

    if content.startswith('/help'):
        await channel.send("") # TODO: コマンドを表示
        
    if content.startswith('!v1'):
        try:
            puuid = fetch_player_id('ねこぜ', 'Prr')
            match_history = fetch_match_history(puuid)
            if len(match_history) == 0:
                await channel.send('直近の対戦履歴にカスタムマッチのデータが見つかりませんでした。')
            else:
                result = dto(match_history)
                left = '左チーム: '
                right = '右チーム: '
                left_index = [0, 3, 4, 7, 8]
                for i in range(len(result)):
                    if i in left_index:
                        left += result[i]['name'] + ' / '
                    else:
                        right += result[i]['name'] + ' / '
                await channel.send(left)
                await channel.send(right)
        except Exception as e:
            await channel.send(f'エラーが発生しました: {e}')

    if content.startswith('!l1'):
        if not author.voice:
            await channel.send("エラー")
            return
        
        voice_channel = author.voice.channel
        members = voice_channel.members
        if members.count < 10:
            await channel.send("エラー")
        # members = [
        #     {
        #         'id': 249593719068688384,
        #         'name': 'sho.ohs',
        #         'global_name': 'SHO',
        #         'bot': False,
        #         'nick': None,
        #         'guild': {
        #             'id': 1262956667310706799,
        #             'name': 'しょおのサーバー',
        #             'shard_id': 0,
        #             'chunked': True,
        #             'member_count': 2
        #         }
        #     },
        #     {
        #         'id': 249593719068688385,
        #         'name': 'john.doe',
        #         'global_name': 'ジョン',
        #         'bot': False,
        #         'nick': 'Johnny',
        #         'guild': {
        #             'id': 1262956667310706800,
        #             'name': 'ジョンのサーバー',
        #             'shard_id': 1,
        #             'chunked': False,
        #             'member_count': 5
        #         }
        #     },
        #     {
        #         'id': 249593719068688386,
        #         'name': 'jane.doe',
        #         'global_name': 'ジェーン',
        #         'bot': False,
        #         'nick': None,
        #         'guild': {
        #             'id': 1262956667310706801,
        #             'name': 'ジェーンのサーバー',
        #             'shard_id': 1,
        #             'chunked': True,
        #             'member_count': 3
        #         }
        #     },
        #     {
        #         'id': 249593719068688387,
        #         'name': 'mike.smith',
        #         'global_name': 'マイク',
        #         'bot': False,
        #         'nick': 'Mikey',
        #         'guild': {
        #             'id': 1262956667310706802,
        #             'name': 'マイクのサーバー',
        #             'shard_id': 2,
        #             'chunked': True,
        #             'member_count': 4
        #         }
        #     },
        #     {
        #         'id': 249593719068688388,
        #         'name': 'lisa.jones',
        #         'global_name': 'リサ',
        #         'bot': False,
        #         'nick': 'LJ',
        #         'guild': {
        #             'id': 1262956667310706803,
        #             'name': 'リサのサーバー',
        #             'shard_id': 2,
        #             'chunked': False,
        #             'member_count': 6
        #         }
        #     },
        #     {
        #         'id': 249593719068688389,
        #         'name': 'tom.brown',
        #         'global_name': 'トム',
        #         'bot': False,
        #         'nick': None,
        #         'guild': {
        #             'id': 1262956667310706804,
        #             'name': 'トムのサーバー',
        #             'shard_id': 3,
        #             'chunked': True,
        #             'member_count': 2
        #         }
        #     },
        #     {
        #         'id': 249593719068688390,
        #         'name': 'sara.davis',
        #         'global_name': 'サラ',
        #         'bot': False,
        #         'nick': 'Sari',
        #         'guild': {
        #             'id': 1262956667310706805,
        #             'name': 'サラのサーバー',
        #             'shard_id': 3,
        #             'chunked': False,
        #             'member_count': 8
        #         }
        #     },
        #     {
        #         'id': 249593719068688391,
        #         'name': 'bob.miller',
        #         'global_name': 'ボブ',
        #         'bot': False,
        #         'nick': 'Bobby',
        #         'guild': {
        #             'id': 1262956667310706806,
        #             'name': 'ボブのサーバー',
        #             'shard_id': 4,
        #             'chunked': True,
        #             'member_count': 7
        #         }
        #     },
        #     {
        #         'id': 249593719068688392,
        #         'name': 'kate.wilson',
        #         'global_name': 'ケイト',
        #         'bot': False,
        #         'nick': None,
        #         'guild': {
        #             'id': 1262956667310706807,
        #             'name': 'ケイトのサーバー',
        #             'shard_id': 4,
        #             'chunked': False,
        #             'member_count': 9
        #         }
        #     },
        #     {
        #         'id': 249593719068688393,
        #         'name': 'alice.lee',
        #         'global_name': 'アリス',
        #         'bot': False,
        #         'nick': 'Ali',
        #         'guild': {
        #             'id': 1262956667310706808,
        #             'name': 'アリスのサーバー',
        #             'shard_id': 5,
        #             'chunked': True,
        #             'member_count': 10
        #         }
        #     }
        # ]
        random.shuffle(members)

        global_names = [member['global_name'] for member in members]
        
        blue_side = global_names[::2]
        red_side = global_names[1::2]
        
        
        blue_side_str = '\n'.join(blue_side)
        red_side_str = '\n'.join(red_side)
        output = f"**ブルーサイド**\n{blue_side_str}\n\n**レッドサイド**\n{red_side_str}"
        
        await channel.send(output)
        
        
    if content.startswith('!l2'):
        if not author.voice:
            await channel.send("You are not in a voice channel.")
            return
        
        voice_channel = author.voice.channel
        members = voice_channel.members
        # TODO: チームとロールを分ける
        member_names = ', '.join([member.name for member in members])
        await channel.send(f'Users in {voice_channel.name}: {member_names}')

    if content.startswith('!l3'):
        champions = get_champions()
        await channel.send(champions)
        
bot.run(DISCORD_BOT_TOKEN)
