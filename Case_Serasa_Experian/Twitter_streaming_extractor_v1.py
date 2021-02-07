from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler

import json
import socket

class Tweet():
    tweet_id: str = None
    created_at: str = None
    text: str = None
    hashtags: str = None
    retweet_count: int = None
    possibly_sensitive: bool = None
    lang: str = None
    user_id: str = None
    user_name: str = None
    user_description: str = None
    user_verification: bool = None
    user_followers_count: int = None
    user_friends_count: int = None
    user_created_at: str = None
    user_location: str = None

    def get_json(self):
        json_data = {
            'tweet_id':self.tweet_id,
            'created_at':self.created_at,
            'text':self.text,
            'hashtags':self.hashtags,
            'retweet_count':self.retweet_count,
            'possibly_sensitive':self.possibly_sensitive,
            'lang':self.lang,
            'user_id':self.user_id,
            'user_name':self.user_name,
            'user_description':self.user_description,
            'user_verification':self.user_verification,
            'user_followers_count':self.user_followers_count,
            'user_friends_count':self.user_friends_count,
            'user_created_at':self.user_created_at,
            'user_location':self.user_location,
        }
        return json_data

class TwitterListener(StreamListener):
    def __init__(self, client_socket):
        self.client_socket = client_socket
    
    def constructor(self, data):
        tweet = Tweet()
        hashtags = ""
        for h in data["entities"]["hashtags"]:
            hashtags = h["text"] + ", " + hashtags
        tweet.id = data["id"]
        tweet.created_at = data["created_at"]
        tweet.text = data['extended_tweet']['full_text'] if "extended_tweet" in data else data["text"]
        tweet.user_id = data["user"]["id"]
        tweet.hashtags = hashtags
        tweet.retweet_count = data["retweet_count"]
        tweet.possibly_sensitive = data['possibly_sensitive'] if "possibly_sensitive" in data else None
        tweet.lang = data["lang"]
        tweet.user_id = data["user"]["id"]
        tweet.user_name = data["user"]["name"]
        tweet.user_description = data["user"]["description"]
        tweet.user_verification = data["user"]["verified"]
        tweet.user_followers_count = data["user"]["followers_count"]
        tweet.user_friends_count = data["user"]["friends_count"]
        tweet.user_created_at = data["user"]["created_at"]
        tweet.user_location = data["user"]["location"]
        return tweet
    
    def on_data(self, data):
        try:
            json_data = json.loads(data)
            print(json_data["text"])
            tweet = self.constructor(json_data)
            self.client_socket.send(str(tweet.get_json()).encode('utf-8')+"t_end")
        except BaseException as e:
            print("Error: " + str(e))
        return True
    
    def on_error(self, status_code):
        print(status_code)
        return True

def authentication():
    PATH = "D:/William/Computação/Data Science/Cases/SerasaExperian/{0}"
    
    API_KEY = open(file=PATH.format("API_key.txt"), mode="r", encoding="UTF-8").read()
    API_SECRET_KEY = open(file=PATH.format("API_secret_key.txt"), mode="r", encoding="UTF-8").read()
    ACCESS_TOKEN = open(file=PATH.format("access_token.txt"), mode="r", encoding="UTF-8").read()
    ACCESS_TOKEN_SECRET = open(file=PATH.format("access_token_secret.txt"), mode="r", encoding="UTF-8").read()
    
    auth = OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth

def sendData(client, keywords, languages):
    print('authenticating...')
    auth = authentication()
    print('start twitter listener...')
    twitter_listener = TwitterListener(client_socket=client)
    print('start twitter streaming...')
    twitter_stream = Stream(auth=auth, listener=twitter_listener)
    print("start twitter streaming...")
    twitter_stream.filter(track=keywords, is_async=False, languages=languages)

if __name__ == "__main__":
    skt = socket.socket()
    host = "localhost"
    port = 5555
    skt.bind((host, port))
    print('socket is ready')
    skt.listen(4)
    print('socket is listening')
    client, address = skt.accept()
    print("Received request from: " + str(address))
    # select here the keyword for the tweet data
    sendData(client=client, keywords=['COVID'], languages=["en"])