import discord, json, asyncio, datetime
from core.classes import Cog_Extension
from discord.ext import commands
with open ('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Countdown(Cog_Extension):

    async def countdown(self):
        TPE_time = datetime.timezone(datetime.timedelta(hours=8))
        deadline = datetime.date(2024, 7, 19)
        morning = datetime.time(6, 30).strftime('%H%M')
        channel = await self.bot.fetch_channel(int(jdata['countdown_channel']))
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            ntime = datetime.datetime.now(tz=TPE_time).strftime('%H%M')
            nowtime = datetime.datetime.now(tz=TPE_time).strftime('%I:%M:%S %p')
            today = datetime.datetime.now(tz=TPE_time).strftime('%Y - %m - %d')
            utctoday = datetime.date.today()
            rest_day = (deadline - utctoday).days

            if ntime == morning and rest_day >= -1:
                if rest_day == -1:      #blue
                    color = 0x3498db
                elif rest_day == 0:     #blue
                    color = 0x3498db
                elif rest_day == 1:     #purple
                    color = 0x8b00ff
                elif rest_day <= 5:     #red
                    color = 0xff0000
                elif rest_day <= 14:    #orange
                    color = 0xff8c00
                elif rest_day <= 30:    #yellow
                    color = 0xffd700
                elif rest_day <= 50:    #yellow green
                    color = 0xadff2f
                else:                   #green
                    color = 0x66e100

                EMB = discord.Embed(title="今日日期 :",description=today,color=color)
                EMB.set_author(name="倒數")
                EMB.add_field(name="還有 :", value="", inline=True)
                EMB.add_field(name=f"{rest_day} 天", value="", inline=True)
                EMB.set_footer(text=nowtime)
                await channel.send(embed=EMB)
                await asyncio.sleep(60)
            await asyncio.sleep(5)

    @commands.Cog.listener()
    async def on_ready(self):
        countdown_task = await self.bot.loop.create_task(self.countdown())


async def setup(bot):
    await bot.add_cog(Countdown(bot))
