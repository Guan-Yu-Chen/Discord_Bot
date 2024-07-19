import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Main(Cog_Extension):

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} ms')

    @commands.command()
    async def rosemary(self, ctx):
        pic = discord.File(jdata['rosemary_icon'])
        await ctx.send(file = pic)
    
    @commands.command()
    async def embed(self, ctx):
        embed=discord.Embed(title="HI", url=jdata["rick_roll_jpg"], description="Don't click the \"HI\"")
        embed.set_author(name="none")
        embed.add_field(name="Hi", value="this is a hi", inline=False)
        embed.set_footer(text="666")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def repeat(self, ctx, *,msg):
        await ctx.send(msg)

    @commands.command()
    async def say(self, ctx, *,msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    async def purge(self, ctx, num):
        print(num)
        await ctx.message.delete(limit=num+1)


async def setup(bot):
    await bot.add_cog(Main(bot))
