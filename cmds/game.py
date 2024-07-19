import discord, json
from discord.ext import commands
from core.classes import Cog_Extension
import random

with open('setting.json', 'r', encoding = 'utf8') as jfile:
    jdata = json.load(jfile)

class Game(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.active_games = {}

    @commands.command()
    async def roll(self, ctx, num: int):
        x = random.randint(1, num)
        await ctx.send(f"Result: {x}")

    @commands.command()
    async def guess(self, ctx, max_num = 99, max_attempt = 5):
        if str(ctx.channel.id) != jdata['test_channel']:
            return
        
        user_id = ctx.author.id
        num = random.randint(1, max_num)
        if user_id not in self.active_games:
            self.active_games[user_id] = {
                'num' : num,
                'max_attempt' : max_attempt,
                'attempts' : 0
            }
            await ctx.send(f"Guess a number from 1 to {max_num}:")
        return
    
    async def guess_number(self, message):
        if str(message.channel.id) != jdata['test_channel']:
            return
        if not message.author.id in self.active_games:
            return
        
        user_id = message.author.id
        user_name = message.author.nick
        info = self.active_games[user_id]
        num = info['num']
        guess = int(message.content)
        info['attempts'] += 1

        if guess == num:
            await message.channel.send(f"**{user_name}**, you find the number! The number is **{num}**!")
            self.active_games.pop(user_id)
            return
        
        chance = info['max_attempt'] - info['attempts']
        if chance > 0:
            if guess > num:
                await message.channel.send(f"**{user_name}**, the number is **smaller than {guess}**, you still have **{chance} more chance**")
            else:
                await message.channel.send(f"**{user_name}**, the number is **greater than {guess}**, you still have **{chance} more chance**")
        else:
            self.active_games.pop(user_id)
            await message.channel.send(f"**{user_name}**, you **lose** the game! The number is **{num}**!")

async def setup(bot):
    await bot.add_cog(Game(bot))
