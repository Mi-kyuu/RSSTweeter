import PySimpleGUI as sg

from time import sleep
import datetime
import schedule
import json
from requests_oauthlib import OAuth1Session #OAuthライブラリの読み込み

import feedparser

update_url = "https://api.twitter.com/1.1/statuses/update.json" #ツイートポストエンドポイント

RSS_URL = ''

# Option設定とLayout
sg.theme('Dark Teal 12')

layout = [
    [sg.Text('RSS Tweeter')],
    [sg.Text('CONSUMER_KEY', size=(21, 1)), sg.InputText('',size=(40, 1))],
    [sg.Text('CONSUMER_SECRET', size=(21, 1)), sg.InputText('',size=(40, 1))],
    [sg.Text('ACCESS_TOKEN', size=(21, 1)), sg.InputText('',size=(40, 1))],
    [sg.Text('ACCESS_TOKEN_SECRET', size=(21, 1)), sg.InputText('',size=(40, 1))],
    [sg.Text('RSSURL', size=(21, 1)), sg.InputText('', size=(40,1))],
    [sg.Text('Tweet Time(HH:MM)', size=(21, 1)), sg.InputText('', size=(40,1))],
    [sg.Text('', size=(21, 1)), sg.Submit(button_text='Schedule!!', size=(35, 1))]
]

print("RSS Tweeter")
print("必要事項を入力し、Schedule!!ボタンを押すと予約されます")

# Window生成
window = sg.Window('RSS Tweeter', layout)

def tweet():
     twitter = OAuth1Session(CK, CS, AT, ATS)

     d = feedparser.parse(RSS_URL) #feedの取得
     body = ""
     cnt = 0
     for entry in d.entries:
         body = entry.title +"\n"+ entry.link
         print(body)
         cnt += 1
         if cnt == 1: #feedの先頭だけ取得
             break
          
     twtime =  datetime.datetime.now()
     print("\n")
     print(twtime) #取得日時を表示
     
     params = {"status" : body}
     res = twitter.post(update_url, params = params)
     if res.status_code == 200: #200:成功
       print("\nTweet Success")
     else:  #200じゃなかったら失敗
            print('\nTweet Failed. Code : %d' %res.status_code)


#Event
while True:
    event, values = window.read()

    if event is None:
        break

    if event == 'Schedule!!':  #ボタンが押されたらSchedule開始
        if  (values[0] == "" or values[1] == "" or values[2] == "" or values[3] == "" or values[4] == "" or values[5] == ""):
             print("未入力の箇所があります")
             continue
        
        CK =  values[0]
        CS =  values[1]
        AT =  values[2]
        ATS = values[3]
        twitter = OAuth1Session(CK, CS, AT, ATS)  #認証処理

        RSS_URL = values[4]

        schedule.every().day.at(values[5]).do(tweet) #指定時刻にスケジュール

        print("毎日 %s に予約されました" %values[5])
        print("RSS_URL: %s" %values[4])
        print("このコンソールを閉じると予約が解除され、アプリケーションが終了します")
        
        window.close() #Window閉じる

        #Main loop
        while True:
            schedule.run_pending()
            sleep(56) #56秒待つ
        
    

#終了処理
window.close()
