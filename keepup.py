# -*- coding: utf-8 -*-
import os
from requests_oauthlib import OAuth1Session
from datetime import datetime, timedelta, timezone
import json
#import passfile

# keys
CK = os.environ.get('CONSUMER_KEY')
CSK = os.environ.get('CONSUMER_SECRET_KEY')
AT = os.environ.get('ACCESS_TOKEN')
ATS = os.environ.get('ACCESS_TOKEN_SECRET')
#test
#CK = passfile.CONSUMER_KEY
#CSK = passfile.CONSUMER_SECRET_KEY
#AT = passfile.ACCESS_TOKEN
#ATS = passfile.ACCESS_TOKEN_SECRET

twitter = OAuth1Session(CK, CSK, AT, ATS)

now = datetime.now()
ystd = now - timedelta(days=1)

now_y = int(now.strftime('%Y'))
now_m = int(now.strftime('%m'))
now_d = int(now.strftime('%d'))
ystd_y = int(ystd.strftime('%Y'))
ystd_m = int(ystd.strftime('%m'))
ystd_d = int(ystd.strftime('%d'))

UTC = timezone.utc
JST = timezone(timedelta(hours=+9), 'JST')

#日本時間
#本日の0時-1秒 ＝　昨日の23:59:59以前
until_date_time = datetime(now_y, now_m, now_d, tzinfo=JST) - timedelta(seconds=1)
#昨日の00:00:00以降
since_date_time = datetime(ystd_y, ystd_m, ystd_d, tzinfo=JST) 

#print(until_date_time)
#print(since_date_time)

# 指定時間
timestamp_max = int(until_date_time.replace(tzinfo=UTC).timestamp() * 1000 - 1288834974657)
timestamp_since = int(since_date_time.replace(tzinfo=UTC).timestamp()  * 1000 - 1288834974657)

# 22ビットシフト
max_id = timestamp_max << 22
since_id = timestamp_since << 22

url_search = "https://api.twitter.com/1.1/statuses/user_timeline.json"
url_postname = "https://api.twitter.com/1.1/account/update_profile.json"

# max_id, since_idの指定
#params_search ={'since_id': since_id, 'count': 20, 'screen_name':'kantei', 'include_rts':False, 'exclude_replies': True}
params_search ={'since_id': since_id, 'screen_name':'自分のID', 'include_rts':False, 'exclude_replies': True}

#search_word = '総理'
search_word = '#勉強した'

win_emoji = '🌿'
lose_emoji = '🍂'

#絵文字投稿
def update_name(search_result):
    if search_result == True:
        emoji = win_emoji
    else:
        emoji = lose_emoji
    username = 'ユーザ名' + emoji
    params_postname ={'name':username}
    req = twitter.post(url_postname, params=params_postname)

#if __name__ == "__main__":
def lambda_handler(event, context):
    req = twitter.get(url_search, params = params_search)
    if req.status_code == 200:
        res = json.loads(req.text)
        #print(res)
        for line in res:
            if search_word in line['text']:
                print('OK!')
                search_result = True
                break
            else:
                print('NO...')
                search_result = False
        update_name(search_result)