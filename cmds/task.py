import discord , json, asyncio, datetime
from core.classes import Cog_Extension
from discord.ext import commands

class Task(Cog_Extension):

    @commands.command()
    async def stime(self, ctx, time):
        with open ('setting.json','r',encoding='utf8') as jfile:
            jdata = json.load(jfile)
        self.channel = await self.bot.fetch_channel(int(jdata['test_channel']))
        with open ('setting.json','r',encoding='utf8') as jfile:
            jdata = json.load(jfile)
        jdata['time'] = time
        with open ('setting.json','w',encoding='utf8') as jfile:
            json.dump(jdata, jfile, indent=4)
        self.stime = str(jdata['time'])
        await self.channel.send(f'Time set : {time}')
    
    async def t1(self):
        await self.bot.wait_until_ready()
        TPE_time = datetime.timezone(datetime.timedelta(hours=8))
        while not self.bot.is_closed():
            self.ntime = datetime.datetime.now(tz=TPE_time).strftime('%H%M')
            if self.ntime == self.stime:
                await self.channel.send(f'It\'s {self.stime} now.')
                await asyncio.sleep(60)
            else:
                await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_ready(self):
        self.t1_task = await self.bot.loop.create_task(self.t1())
       
async def setup(bot):
    await bot.add_cog(Task(bot))
