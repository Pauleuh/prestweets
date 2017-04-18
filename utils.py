import json
import datetime


def get_all_tweets_from_user(api, user_name, min_id=None):
    all_tweets = []
    if not min_id:
        first_tweets = api.GetUserTimeline(screen_name=user_name)
    else:
        first_tweets = api.GetUserTimeline(screen_name=user_name, since_id=min_id)
    if not len(first_tweets):
        return all_tweets
    all_tweets += [tweet.AsDict() for tweet in first_tweets]

    max_id = all_tweets[-1]['id']
    not_done = True
    while not_done:
        if not min_id:
            tweets = api.GetUserTimeline(screen_name=user_name, max_id=max_id)
        else:
            tweets = api.GetUserTimeline(screen_name=user_name, max_id=max_id, since_id=min_id)

        if len(tweets) > 1:

            for tweet in tweets:
                all_tweets.append(tweet.AsDict())
            max_id = str(int(all_tweets[-1]['id']) - 1)

        else:
            not_done = False
    return all_tweets


accounts = {
    "meluche": ["JLMelenchon"],
    "macron": ["EmmanuelMacron"],
    "lepen": ["MLP_officiel"],
    "hamon": ["benoithamon"],
    "fillon": ["FrancoisFillon"]
}


def update_tweets_for_users(api):
    with open("tweets.json", "r") as tweetfile:
        all_tweets_dict = json.load(tweetfile)
    for account, usernames in accounts.iteritems():
        print account

        latest_id = find_latest_id(account, all_tweets_dict)
        print latest_id
        new_tweets = get_all_tweets_from_user(api, usernames[0], min_id=latest_id)
        all_tweets_dict[account] += new_tweets

        all_tweets_dict[account] = sorted(all_tweets_dict[account], key=lambda k: datetime.datetime.strptime(k["created_at"][4:], "%b %d %H:%M:%S +0000 %Y"), reverse=True)

    with open("tweets.json", "w") as myfile:
        json.dump(all_tweets_dict, myfile)


def find_latest_id(user_name, tweets):
    # sort in case

    return sorted(tweets[user_name], key=lambda k: datetime.datetime.strptime(k["created_at"][4:], "%b %d %H:%M:%S +0000 %Y"), reverse=True)[0]['id']

