    client_id = client_ID
    client_secret = client_SECRET
    messege = ctx.content.replace("!t  ", "")
    encQuery = urllib.parse.quote(messege)
    data = "query=" + encQuery
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read().decode('utf-8')
    else:
        print("Error Code:" + rescode)
    if len(ctx.content) < 500:
        if ctx.content.startswith("!kj "):
            if ctx.author.bot: return None
            encText = urllib.parse.quote(messege)
            data = "source=ko&target=ja&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_ID)
            request.add_header("X-Naver-Client-Secret",client_SECRET)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                result = response_body.decode('utf-8')
                result = json.loads(result)
                translated = result['message']['result']["translatedText"]
                final = translated.replace("['", "").replace("']", "")
            else:
                print("Error Code:" + rescode)
            await ctx.channel.send(final)

        elif ctx.content.startswith("!jk "):
            if ctx.author.bot: return None
            encText = urllib.parse.quote(messege)
            data = "source=ja&target=ko&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_ID)
            request.add_header("X-Naver-Client-Secret",client_SECRET)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                result = response_body.decode('utf-8')
                result = json.loads(result)
                translated = result['message']['result']["translatedText"]
                final = translated.replace("'['", "").replace("']", "")
            else:
                print("Error Code:" + rescode)
            await ctx.channel.send(final)
        else:
            print("예외")
        return
    else:
        await ctx.channel.send("[ERROR]\n500자 이내로 작성 해 주십시오.\n100文字以内で作成して下さい。")