import discord
from discord.ext import commands
import urllib.request
import json
bot = commands.Bot(command_prefix='')
TOKEN = 'NzgzNDkxNjk0MjcyMTg0MzYx.X8bhgA.8KPGrRXRQUrrV9xEye4pwVHLIr8'
client_ID = "bbVOGQumI6XjRgjy0xKf"
client_SECRET = "i3iMBqJXF1"


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Translate'))
    print(f"New log in as {bot.user}")

@bot.event
async def on_message(ctx):

    if ctx.content.startswith("!t "):
        message = ctx.content.replace("!t ", "")

        if len(message) < 500:
            encQuery = urllib.parse.quote(message)
            data = "query=" + encQuery
            request = urllib.request.Request("https://openapi.naver.com/v1/papago/detectLangs")
            request.add_header("X-Naver-Client-Id",client_ID)
            request.add_header("X-Naver-Client-Secret",client_SECRET)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()

            if(rescode==200):
                response_body = response.read().decode('utf-8')
                res_json = json.loads(response_body)

                if res_json['langCode'] == "ko":
                    sourceLang = "ko"
                    targetLang = "ja"
                    targetLang2 = "en"

                elif res_json['langCode'] == "ja":
                    sourceLang = "ja"
                    targetLang = "ko"
                    targetLang2 = "en"

                elif res_json['langCode'] == "en":
                    sourceLang = "en"
                    targetLang = "ko"
                    targetLang2 = "ja"

                else:
                    await ctx.channel.send(f"Detected language : '{res_json['langCode'].upper()}'\n지원하지 않는 언어입니다.\n対応していない言語です。")
                    return

                encText = urllib.parse.quote(message)
                data = f"source={sourceLang}&target={targetLang}&text=" + encText
                data2 = f"source={sourceLang}&target={targetLang2}&text=" + encText
                request = urllib.request.Request("https://openapi.naver.com/v1/papago/n2mt")
                request.add_header("X-Naver-Client-Id",client_ID)
                request.add_header("X-Naver-Client-Secret",client_SECRET)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                response2 = urllib.request.urlopen(request, data=data2.encode("utf-8"))
                rescode = response.getcode()
                rescode2 = response2.getcode()
                if(rescode==200 and rescode2==200):
                    response_body = response.read().decode('utf-8')
                    response_body2 = response2.read().decode('utf-8')
                    result = json.loads(response_body)
                    result2 = json.loads(response_body2)
                    final = result['message']['result']["translatedText"].replace("'['", "").replace("']", "")
                    final2 = result2['message']['result']["translatedText"].replace("'['", "").replace("']", "")

                    await ctx.channel.send(final + "\n" + final2)
                    return
                        
                else:
                    print("Error Code:" + rescode)
                    return

            else:
                print("Error Code:" + rescode)
                return

        else:
            await ctx.channel.send("[ERROR]\n500자 이내로 작성 해 주십시오.\n100文字以内で作成して下さい。")
            return

    else:
        return

bot.run(TOKEN)