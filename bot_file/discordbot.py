import discord
from discord.ext import tasks
from datetime import datetime as dt
import time
import sys
import pro_info as info
#以下を自分の環境に合わせたパスに変更してください。
proInfoPath="C:/xxxx/xxxx/bot_file/pro_info.py"

# 自分のBotのアクセストークンに置き換える
TOKEN = 'XXXXXX'
#発言させたいチェンネルIDに置き換える
CHANNEL_ID= 000000
#発言させたい時間に変更　例:"22:40"
sayTime="22:40"

#ディレクトリにある xxx.py ファイルをインポート
sys.path.append(proInfoPath)

intents = discord.Intents.default()
intents.message_content = True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=discord.Intents.all())

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    #ループ処理実行
    loop.start()
    print('ログインしました')

#60秒毎に処理
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = dt.now().strftime('%H:%M')
    #発言時間になったらif分の処理を行う
    if now == sayTime:
        #コンテスト時間の処理
        if len(info.abctime)!=0:
            queabctime=info.abctime[0][5:7]+"月"+info.abctime[0][8:10]+"日"+info.abctime[0][11:-3]
        elif len(info.actime)==0:
            queabctime="予定されていません"
        if len(info.ahctime)!=0:
            queahctime=info.ahctime[0][5:7]+"月"+info.ahctime[0][8:10]+"日"+info.ahctime[0][11:-3]
        elif len(info.actime)==0:
            queahctime="予定されていません"

        #コンテスト時間の発言処理
        abc_difftime=str(info.diff_time[0].days)+"日"+str(info.diff_time[0].seconds//3600)+"時間"+str(info.diff_time[0].seconds%3600//60)+"分"
        ahc_difftime=str(info.diff_time[1].days)+"日"+str(info.diff_time[1].seconds//3600)+"時間"+str(info.diff_time[1].seconds%3600//60)+"分"
        text=str("こんばんは。{}をお知らせします。 \n 次のABCは{}\n 次のAHCは{}です。\n \n 次のABC開催まで残り{} \n 次のAHC開催まで残り{} \n".format(now,queabctime,queahctime,abc_difftime,ahc_difftime,ahc_difftime))

        #AC発言処理
        channel_sent = client.get_channel(CHANNEL_ID)
        await channel_sent.send(text)
        text2="\n \n 今日はみんなで{}回問題を解きました。".format(sum(info.TodayACli))
        for i in range(len(info.UserLi)):
            text2+="\n {}回 {}".format(info.TodayACli[i],info.UserLi[i])
        time.sleep(1)
        await channel_sent.send(text2)

        ACsum=0
        for i in info.UserLi:
            ACsum+=int(info.ACdic[i])
        text3="\n \n みんなの合計累計AC数は{}回です ".format(ACsum)
        for i in info.UserLi:
            text3+="\n {}回 {}".format(info.ACdic[i],i)
        time.sleep(1)
        await channel_sent.send(text3)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)