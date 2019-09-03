# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta
#from counter.status import check_limitation

user_id_array, mentioner_id_array, tweet_array = [], [], []

def get_mentions(token):
    url = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'
    params = {'count' : 10}
    res = token.get(url, params = params)
    if res.status_code == 200:
        mentioners = json.loads(res.text)
        for mentioner in mentioners:
            if mentioner['text'].find('カウント') != -1 and not(mentioner['favorited']):
                    user_id_array.append((mentioner['user'])['screen_name'])
                    mentioner_id_array.append(mentioner['id'])
    else:
        exit(1)
        
def post_favorit(token):
    url = 'https://api.twitter.com/1.1/favorites/create.json' 
    for i in range(len(mentioner_id_array)): 
        params = {'id' : mentioner_id_array[i]}
        res = token.post(url, params = params)
        if res.status_code != 200:
            exit(1)


def getdate(con):
    today = datetime.today()
    dt = today - timedelta(con)
    return dt

def postformat(con):
    dt = datetime.today()
    dt = dt - timedelta(con)
    return str.format("{0}/{1}", dt.month, dt.day)

def Searchformat(date):
    return str.format("{0}-{1}-{2}", date.year,
                      date.month, date.day)

def protect_checker(token, user):
    url = 'https://api.twitter.com/1.1/users/show.json'
    params = {'screen_name' : user}
    res = token.get(url, params = params)
    if res.status_code != 200:
        exit(1)
    protect = json.loads(res.text)
    return protect['protected']

def Search_tweet(token, user):
    tweet_vals_array = []
    for i in range(7):
        url = "https://api.twitter.com/1.1/search/tweets.json"
        texts = str.format("from:{0} since:{1} until:{2}", user, Searchformat(getdate(i+1)), Searchformat(getdate(i)))
        params = {'q': texts, 'count' : 100, 'result_type' : "mixed"}
        res = token.get(url, params = params)  
  
        if res.status_code == 200:
            tweeted = json.loads(res.text)
            tweetval = 0
            for tweet in tweeted['statuses']:                
                tweetval += 1
            tweet_vals_array.append(tweetval)
        else:
            exit(1)
    return tweet_vals_array

def post_reply(token, id, text):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    params = {'in_reply_to_status_id' : id, 'status' : text}
    try:
        token.post(url, params = params)
    except:
        exit(1)

def check(token):
    get_mentions(token)
    for i in range(len(user_id_array)):
        if protect_checker(token, user_id_array[i]):
            data = ("@"+ str(user_id_array[i]) +" 非公開のアカウントはカウントできません")
        else:
            text = ""
            tweet_array = Search_tweet(token, user_id_array[i])
            for j in range(len(tweet_array)):                    
                if tweet_array[j] == 100:
                    text = text + postformat(j) + " : 100+" + " ツイート" + "\n"   
                else:
                    text = text + postformat(j) + " : " + str(tweet_array[j]) + " ツイート" + "\n"
            data = ("@"+ str(user_id_array[i]) + " \n" + text)
        post_reply(token, mentioner_id_array[i], data) 
    if len(user_id_array) != 0:
        post_favorit(token)
