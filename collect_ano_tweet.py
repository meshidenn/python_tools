import tweepy
import json
import pandas as pd
import time


def main():
    consumer_key = 'PJ4YjCVOTSLhDQ3rwWpGNkH4q'
    consumer_secret = '7DduoVXvEJu56kEhLGU1O9Lil6RIWa6AsmLEPeGPewR9BhaYJC'
    access_token_key = '1098402262538305536-gkl85nK1wxFybQglkn2N0X8arXQvB6'
    access_token_secret = 'jKu5l0Y5gL4e1SAJ8T5C0w63DmPDthozsKmcAAVrb43rz'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API(auth)

    # for csv
    # df = pd.read_csv("/home/hiroki-iida/data/polarity/inui/tweets_open.csv",
    #                 header=None)
    # status_ids = df.iloc[:, 2].values
    
    # for json
    df = pd.read_json("/home/hiroki-iida/data/polarity/gram/corpus_binary.json",
                      orient='records', lines=True)

    status_ids = df.iloc[:, 1].values

    tweet_list = list()
    error_ids = list()
    limit = 890
    wait = 1

    for i, id in enumerate(status_ids):
        if i >= limit * wait:
            time.sleep(930)
            wait += 1
        
        try:
            tweet_status = api.get_status(id)
        except tweepy.TweepError as e:
            try:
                error_dict = json.loads(e.response.text)
                error_dict["col_id"] = str(i)
                error_dict["status_id"] = str(id)
                print(i, ", ", error_dict)
                error_ids.append(error_dict)
                continue
            except:
                print(e)
        
        tweet_dict = tweet_status._json
        tweet_json = json.dumps(tweet_dict)
        tweet_list.append(tweet_json)

    with open("/home/hiroki-iida/data/polarity/gram/tweets.json",
              "w") as f:
        json.dump(tweet_list, f)

    with open("/home/hiroki-iida/data/polarity/gram/error_id.json",
              "w") as f:
        json.dump(error_ids, f)
            
if __name__ == '__main__':
    main()
        
