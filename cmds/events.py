import discord
from discord.ext import commands
from core.classes import Cog_Extension

import json
with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Events(Cog_Extension):
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(jdata['test_channel']))
        await channel.send(f'{member.mention} 加入伺服器!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(int(jdata['test_channel']))
        await channel.send(f'{member.mention} 離開了...')

    @commands.Cog.listener()
    async def on_message(self, message):

        await self.bot.get_cog("Game").guess_number(message)

        if message.content == '...' and message.author != self.bot.user:
            await message.channel.send('...')
        elif message.content == '早安' and message.author != self.bot.user:
            await message.channel.send('早安 ~')
        elif message.content == 'say my name' and message.author != self.bot.user:
            await message.channel.send('You are Heisenberg.')
        elif self.bot.user.mention in message.content and message.author != self.bot.user:
            await message.channel.send('?')
            
async def setup(bot):
    await bot.add_cog(Events(bot))
