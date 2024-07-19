import discord, asyncio, datetime, re
from discord.ext import commands
from core.classes import Cog_Extension
import requests as req
import json
with open('setting.json', 'r', encoding = 'utf8') as jfile:
    jdata = json.load(jfile)

class Weather(Cog_Extension):

    async def weather_forcast(self):
        TPE_time = datetime.timezone(datetime.timedelta(hours=8))
        morning = datetime.time(6, 30).strftime('%H%M')
        channel = await self.bot.fetch_channel(int(jdata['test_channel']))
        author_code = jdata['author_code']
        url_tainan_1week = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-D0047-079?Authorization={author_code}&downloadType=WEB&format=JSON"
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            nowtime = datetime.datetime.now(tz = TPE_time).strftime('%H%M')
            if nowtime == morning:
                res = req.get(url_tainan_1week)
                obj = json.loads(res.text)
                CityData = obj["cwaopendata"]["dataset"]["locations"]

                for area in CityData["location"]:          # 此縣市的每個鄉鎮市區
                    if area["geocode"] == "67000280":
                        District = f"{CityData['locationsName']} {area['locationName']}"
                        description_1 = area['weatherElement'][-1]['time'][0]['elementValue']['value']
                        description_2 = area['weatherElement'][-1]['time'][2]['elementValue']['value']
                        regex = r'[^。]+(?=。)'                                                # 正規表達式，抓天氣描述(用句號分隔)

                        # 今日的資料
                        Date_1 = area['weatherElement'][-1]['time'][0]['startTime'][5:10]          # 12-31
                        Weather_1 = re.findall(regex, description_1)[0]                  # 晴時多雲 etc.
                        MinT_1 = re.findall(regex, description_1)[2][-6:-4]              # 18
                        MaxT_1 = re.findall(regex, description_1)[2][-3:-1]              # 26
                        PoP_1 = re.findall(regex, description_1)[1][5:]                  # 20%

                        # 明日的資料
                        Date_2 = area['weatherElement'][-1]['time'][2]['startTime'][5:10]          # 01-01
                        Weather_2 = re.findall(regex, description_2)[0]                  # 晴時多雲 etc.
                        MinT_2 = re.findall(regex, description_2)[2][-6:-4]              # 18
                        MaxT_2 = re.findall(regex, description_2)[2][-3:-1]              # 26
                        PoP_2 = re.findall(regex, description_2)[1][5:]                  # 20%

                        # 傳送訊息
                        EMB = discord.Embed(title = " ", description = "今明2日天氣預報", color = 0x3498db)
                        EMB.set_author(name = District, url = "https://www.cwa.gov.tw/V8/C/W/Town/Town.html?TID=6702800")
                        EMB.add_field(name = f"{Date_1[:2]}月{Date_1[-2:]}日", value = " ", inline = False)
                        EMB.add_field(name = Weather_1, value = " ", inline = True)
                        EMB.add_field(name = f"降雨機率 : {PoP_1}", value = " ", inline = True)
                        EMB.add_field(name = f"{MinT_1}°C - {MaxT_1}°C", value = " ", inline = True)
                        EMB.add_field(name = " ", value = "==================================================", inline = False)
                        EMB.add_field(name = " ", value = f"{Date_2[:2]}月{Date_2[-2:]}日", inline = False)
                        EMB.add_field(name = " ", value = Weather_2, inline = True)
                        EMB.add_field(name = " ", value = f"降雨機率 : {PoP_2}", inline = True)
                        EMB.add_field(name = " ", value = f"{MinT_2}°C - {MaxT_2}°C", inline = True)
                        EMB.set_footer(text = f"{datetime.datetime.now(tz = TPE_time).strftime('%Y-%m-%d %H:%M:%S')}")
                        await channel.send(embed=EMB)
                        await asyncio.sleep(100)

            else:
                await asyncio.sleep(5)

    @commands.Cog.listener()
    async def on_ready(self):
        weather_forcast_task = await self.bot.loop.create_task(self.weather_forcast())

async def setup(bot):
    await bot.add_cog(Weather(bot))
