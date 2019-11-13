from bs4 import BeautifulSoup
import json
import requests
import lxml.html
import time

target_url = "want get URL"
dict_str = ""
next_url = ""
comment_data = []
session = requests.Session()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
count = 1
# まず動画ページにrequestsを実行しhtmlソースを手に入れてlive_chat_replayの先頭のurlを入手
html = requests.get(target_url)
soup = BeautifulSoup(html.text, "html.parser")

for iframe in soup.find_all("iframe"):
    if("live_chat_replay" in iframe["src"]):
        next_url= iframe["src"]

while(1):
    try:
        time.sleep(1.2)
        html = session.get(next_url, headers=headers)
        soup = BeautifulSoup(html.text,"lxml")


        # 次に飛ぶurlのデータがある部分をfind_allで探してsplitで整形
        for scrp in soup.find_all("script"):
            if "window[\"ytInitialData\"]" in scrp.text:
                dict_str = scrp.text.split(" = ")[1]

        # javascript表記なので更に整形. falseとtrueの表記を直す
        dict_str = dict_str.replace("false","False")
        dict_str = dict_str.replace("true","True")
        # 辞書形式と認識すると簡単にデータを取得できるが, 末尾に邪魔なのがあるので消しておく（「空白2つ + \n + ;」を消す）
        dict_str = dict_str.rstrip("  \n;")
        # 辞書形式に変換
        dics = eval(dict_str)
        # "https://www.youtube.com/live_chat_replay?continuation=" + continue_url が次のlive_chat_replayのurl
        continue_url = dics["continuationContents"]["liveChatContinuation"]["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
        next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url
        # dics["continuationContents"]["liveChatContinuation"]["actions"]がコメントデータのリスト。先頭はノイズデータなので[1:]で保存
        for samp in dics["continuationContents"]["liveChatContinuation"]["actions"][1:]:
            data = samp.get("replayChatItemAction").get("actions")[0].get("addChatItemAction",{}).get("item",{}).get("liveChatTextMessageRenderer",{}).get("message",{}).get("runs",{})
            if data == {}:
                print("continue")
                continue
            else:
                print("success")
        #コメントのみを取得
            comment_data.append(str(data[0]["text"])+"\n")

            data_time = samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]
        #チャットされた時間
            if data_time == {}:
                print("continue")
                continue
            else:
                print("success")
            comment_data.append(str(data_time)+"\n")
            count += 1
    # next_urlが入手できなくなったら終わり
    except:
        print(count)
        break

# ファイルにコメントデータを書き込む
with open("save_file.txt", mode='w', encoding="utf-8") as f:
    f.writelines(comment_data)