import discord, json
from discord.ext import commands
from core.classes import Cog_Extension

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Role(Cog_Extension):

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 1262760331965632603:
            if str(payload.emoji) == '<:gura_a:851744185416417310>':
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(1260448312750772285)
                await  payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 1262760331965632603:
            if str(payload.emoji) == '<:gura_a:851744185416417310>':
                guild = self.bot.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                role = guild.get_role(1260448312750772285)
                await  user.remove_roles(role)

async def setup(bot):
    await bot.add_cog(Role(bot))
