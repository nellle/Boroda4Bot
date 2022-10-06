import disnake
import pymongo.database
from Core import *
from disnake.ext import commands
from pymongo import MongoClient

from CustomDisnake import ClearEmbed

client = commands.Bot(command_prefix="!", intents=disnake.Intents.all())


@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
@commands.has_permissions(administrator=True)
async def set_win(ctx: commands.Context, team: str, mmr: int):
    if team == "dire":
        win_channel = await client.fetch_channel(get_dire_channel())
    elif team == "radiant":
        win_channel = await client.fetch_channel(get_radiant_channel())

    winners = []

    for member in win_channel.members:
        member2 = await client.fetch_user(member.id)
        r_member = RatingMember(member.id)
        r_member.rating += mmr
        winners.append(member2.mention)

    em = ClearEmbed(title=f'Изменение рейтинга',
                    description=f'**Победители:** ' + ','.join(winners)

                    )

    await ctx.send(embed=em)


@client.command()
@commands.has_permissions(administrator=True)
async def set_channel(ctx: commands.Context, team: str, channel: disnake.VoiceChannel):
    if team == "dire":
        set_dire_channel(channel.id)
        await ctx.send(f"Канал для команды **Сил Тьмы** установлен - {channel.mention}")
    elif team == "radiant":
        set_radiant_channel(channel.id)
        await ctx.send(f"Канал для команды **Сил Света** установлен - {channel.mention}")


@client.command()
async def profile(ctx: commands.Context, member: disnake.Member = None):
    if not member:
        member = ctx.author

    em = ClearEmbed(title=f'Профиль {member.display_name}')
    try:
        em.set_thumbnail(url=member.avatar.url)
    except:
        pass
    r_member = RatingMember(member.id)
    em.description = f"**Рейтинг:** {r_member.rating}"
    await ctx.send(embed=em)


client.run("MTAyNzI2Nzk2MjczNTk1MTk1Mw.G4uZNR.S9jhMIsIhKJBVzy_TSPysTAMPhcAZM3guOZDXg")