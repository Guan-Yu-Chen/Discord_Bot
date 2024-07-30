import discord, json, re, datetime
from discord.ext import commands
from discord.ui import Select, View
from core.classes import Cog_Extension
import requests as req

with open("county.json", "r", encoding = "utf8") as jfile:
    county_data = json.load(jfile)
with open("town.json", "r", encoding = "utf8") as jfile:
    town_data = json.load(jfile)
with open("setting.json", "r", encoding = "utf8") as jfile:
    jdata = json.load(jfile)
with open("county_code.json", "r", encoding = "utf8") as jfile:
    county_code_data = json.load(jfile)


class TownSelect(Select):
    def __init__(self, county):
        self.county = county
        super().__init__(placeholder = "選擇鄉鎮市區")

    async def get_weather(self, town, interaction):
        url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/{county_code_data[self.county]}?Authorization={jdata['author_code']}&locationName={town}&elementName=WeatherDescription&format=JSON"
        res = req.get(url)
        obj = json.loads(res.text)
        descriptions = obj['records']['locations'][0]['location'][0]['weatherElement'][0]['time']
        des_today = descriptions[0]
        if "06:00:00" in descriptions[1]['startTime']:
            des_tomorrow = descriptions[1]
        else:
            des_tomorrow = descriptions[2]
        regex = r'[^。]+(?=。)'
        
        today = {
            "month" : des_today['startTime'][5:7],
            "day" : des_today['startTime'][8:10],
            "weather" : re.findall(regex, des_today['elementValue'][0]['value'])[0],
            "minT" : re.findall(regex, des_today['elementValue'][0]['value'])[2][-6:-4],
            "maxT" : re.findall(regex, des_today['elementValue'][0]['value'])[2][-3:-1],
            "PoP" : re.findall(regex, des_today['elementValue'][0]['value'])[1][5:]
        }
        tomorrow = {
            "month" : des_tomorrow['startTime'][5:7],
            "day" : des_tomorrow['startTime'][8:10],
            "weather" : re.findall(regex, des_tomorrow['elementValue'][0]['value'])[0],
            "minT" : re.findall(regex, des_tomorrow['elementValue'][0]['value'])[2][-6:-4],
            "maxT" : re.findall(regex, des_tomorrow['elementValue'][0]['value'])[2][-3:-1],
            "PoP" : re.findall(regex, des_tomorrow['elementValue'][0]['value'])[1][5:]
        }

        EMB = discord.Embed(title = " ", description = "今明2日天氣預報", color = 0x3498db)
        EMB.set_author(name = f"{self.county} {town}")
        EMB.add_field(name = f"{today['month']}月{today['day']}日", value = " ", inline = False)
        EMB.add_field(name = today['weather'], value = " ", inline = True)
        EMB.add_field(name = f"降雨機率 : {today['PoP']}", value = " ", inline = True)
        EMB.add_field(name = f"{today['minT']}°C - {today['maxT']}°C", value = " ", inline = True)

        EMB.add_field(name = " ", value = "==================================================", inline = False)
        EMB.add_field(name = " ", value = f"{tomorrow['month']}月{tomorrow['day']}日", inline = False)
        EMB.add_field(name = " ", value = tomorrow['weather'], inline = True)
        EMB.add_field(name = " ", value = f"降雨機率 : {tomorrow['PoP']}", inline = True)
        EMB.add_field(name = " ", value = f"{tomorrow['minT']}°C - {tomorrow['maxT']}°C", inline = True)
        EMB.set_footer(text = f"{datetime.datetime.now(tz = datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')}")

        await interaction.channel.send(embed = EMB)

class CountySelect(Select):
    def __init__(self):
        self.town_id = ""
        super().__init__(placeholder = "選擇縣市")
        for county in county_data:
            self.add_option(
                label = f"{county['Name']['C']}", 
                description = f"{county['Name']['E']}", 
                value = f"{county['ID']}"
            )

    async def callback(self, interaction):
        id = self.values[0]
        for county in county_data:
            if county['ID'] == id:
                county_name = county['Name']['C']

        town_select = TownSelect(county_name)
        town_select2 = TownSelect(county_name)
        view = View()
        if len(town_data[id]) > 25:
            for town in town_data[id][:24]:
                town_select.add_option(
                    label = f"{town['Name']['C']}", 
                    description = f"{town['Name']['E']}"
                )
            town_select.add_option(
                label = "下一頁", 
                description = "Next Page", 
                value = "+1"
            )
            for town in town_data[id][24:]:
                town_select2.add_option(
                    label = f"{town['Name']['C']}", 
                    description = f"{town['Name']['E']}"
                )
            town_select2.add_option(
                label = "上一頁", 
                description = "Previous Page", 
                value = "-1"
            )
        else:
            for town in town_data[id]:
                town_select.add_option(
                    label = f"{town['Name']['C']}", 
                    description = f"{town['Name']['E']}"
                )
        
        view.add_item(town_select)
        await interaction.response.edit_message(content = f"已選: {county_name}", view = view)

        async def town_callback(interaction):
            if town_select.values[0] == "+1":
                view.clear_items()
                view.add_item(town_select2)
                await interaction.response.edit_message(content = f"已選: {county_name}", view = view)
            else:
                town_select.disabled = True
                await interaction.response.edit_message(content = f"已選: {county_name}", view = view)
                await interaction.followup.send(f"{town_select.values[0]} 天氣預報")
                town = town_select.values[0]
                await town_select.get_weather(town, interaction)

        async def town_callback2(interaction):
            if town_select2.values[0] == "-1":
                view.clear_items()
                view.add_item(town_select)
                await interaction.response.edit_message(content = f"已選: {county_name}", view = view)
            else:
                town_select2.disabled = True
                await interaction.response.edit_message(content = f"已選: {county_name}", view = view)
                await interaction.followup.send(f"{town_select2.values[0]} 天氣預報")
                town = town_select2.values[0]
                await town_select.get_weather(town, interaction)
                
        town_select.callback = town_callback
        town_select2.callback = town_callback2

class Weather(Cog_Extension):

    @commands.command()
    async def weather(self, ctx):
        county_select = CountySelect()

        view = View()
        view.add_item(county_select)
        await ctx.send(view = view)
        
async def setup(bot):
    await bot.add_cog(Weather2(bot))
