import requests

#以下のcontestPathを自分の環境に合わせたパスに変更してください。
contestPath="C:/xxxx/xxxx/bot_file/info_save/contest.html"

#AtcoderのURL
url_contest="https://atcoder.jp/contests/"

site_data = requests.get(url_contest)

#コンテストのhtmlを保存する場所を指定
with open(contestPath, "w",encoding="UTF-8") as f:
    f.write(site_data.text)
    print("書き込みが完了しました")
