import discord
from discord.ext import commands
import json
import os
import asyncio
with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='+',intents=intents)

@bot.event
async def on_ready():
    print(">>> Bot is online! <<<")

@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} loaded.')
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} unloaded.')
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} reloaded.')

async def main():
    for filename in os.listdir('./cmds'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cmds.{filename[:-3]}')
    await bot.start(jdata["rosemary_token"])

if __name__ == "__main__":
    asyncio.run(main())
