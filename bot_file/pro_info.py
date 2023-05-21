from bs4 import BeautifulSoup
from datetime import datetime as dt
import time
import requests
import os
import json

#以下を自分の環境に合わせたパスに変更してください。
contestPath="C:/xxxx/xxxx/bot_file/info_save/contest.html"
ACdicPath="C:/xxxx/xxxx/bot_file/info_save/ACdic.txt"
infoPath="C:/xxxx/xxxx/bot_file/info_save/"

#このUserLiにAtcoderの名前を正確に入力。例：UserLi=["tamakoma","chokudai"]
UserLi=[]


#コンテスト情報の加工
with open(contestPath,encoding="UTF-8") as f:
    data_contest=f.read()
soup = BeautifulSoup(data_contest, "html.parser")

contest_li=[]
elems=soup.select("#contest-table-upcoming > div > div > table > tbody")
tr=[t.find_all("tr") for t in elems]
tr=tr[0]
li=[]
#「\n」を「くくく」に変換（くくくの理由は文章に入ってこなさそうだから）
for i in tr:
    li.append(i.get_text().replace("\n","くくく"))
li_2=[]
#「く」でリストを分けて、空白なら消す
for i in li:
    li_2.append([j for j in i.split("くくく") if j!=""])

abctime=[]
ahctime=[]
for i in li_2:
    if "AtCoder Beginner Contest" in i[3]:
        abctime.append(i[0][:-5])
    if "AtCoder Heuristic Contest" in i[3]:
        ahctime.append(i[0][:-5])

if len(ahctime)==0:
    ahctime.append("2000-02-18 12:00:00")

now = dt.now()
abctime_diff=dt.strptime(abctime[0], '%Y-%m-%d %H:%M:%S')
ahctime_diff=dt.strptime(ahctime[0], '%Y-%m-%d %H:%M:%S')
diff_time=[]
diff_time.append(abctime_diff-now)
diff_time.append(ahctime_diff-now)
for i in diff_time:
    print(str(i.days)+"日"+str(i.seconds//3600)+"時間"+str(i.seconds%3600//60)+"分")
    print(i)
print(ahctime[0])


#Atcoderの提出状況処理

#現在時刻を秒で取得
Enow=int(time.time())
#現在時刻から1日分の秒を引き、その時刻以降のデータを取得に利用
EY=Enow-86400
dtY=dt.fromtimestamp(Enow-86400)

#今日のAC数を記録する箱
TodayACli=[]

#もし初回起動だったら
if not os.path.isfile(ACdicPath):
    print("1回目")
    ACdic={}
    for i in UserLi:
        ACdic[i]=0
    #各ユーザの情報を取得する
    for i in range(len(UserLi)):
        ACcnt=0
        #UserLiに入れられた名前から各APIに接続するためのURLを生成
        userName=UserLi[i]
        userURL="https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user="+userName+"&from_second=0"

        #情報の取得
        ACtx=requests.get(userURL)

        data = ACtx.json()

        with open(infoPath+userName+".json", "w",encoding="UTF-8") as f:
            json.dump(data, f)
            print("書き込みが完了しました")

        testli = data
        for j in testli:
            if j["result"]=="AC":
                ACcnt+=1
        TodayACli.append(ACcnt)
        if userName in ACdic:
            ACdic[userName]+=ACcnt
        else:
            ACdic[userName]=ACcnt
        #スクレイピングしているので、必ず1秒の間隔を空ける
        time.sleep(1)

#2回目以降はこちら
else:
    print("2回目")
    with open(ACdicPath,encoding="UTF-8") as f:
        ACdic=f.read()
        ACdic=json.loads(ACdic)

    #各ユーザの情報を取得する
    for i in range(len(UserLi)):
        ACcnt=0
        #UserLiに入れられた名前から各APIに接続するためのURLを生成
        userName=UserLi[i]
        if userName  not in ACdic:
            userURL="https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user="+userName+"&from_second=0"
        else:
            userURL="https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user="+userName+"&from_second="+str(EY)
        #情報の取得
        ACtx=requests.get(userURL)

        data = ACtx.json()

        with open(infoPath+userName+".json", "w",encoding="UTF-8") as f:
            json.dump(data, f)
            print("書き込みが完了しました")

        testli = data
        for j in testli:
            if j["result"]=="AC":
                ACcnt+=1
        TodayACli.append(ACcnt)
        if userName in ACdic:
            ACdic[userName]=int(ACdic[userName])+ACcnt
        else:
            ACdic[userName]=ACcnt
        #スクレイピングしているので、必ず1秒の間隔を空ける
        time.sleep(1)



with open(ACdicPath, "w",encoding="UTF-8") as f:
    f.writelines(json.dumps(ACdic))

    print("書き込みが完了しました")
