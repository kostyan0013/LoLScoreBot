import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
from time import sleep
import oauth, tweepy, sys, locale, threading, time
from riotwatcher import RiotWatcher, RUSSIA, LoLException, error_404, error_429

access_key = '<your-access-key>'
access_secret = '<your-access-key-secret>'
consumer_key = '<your-consumer-key>'
consumer_secret = '<your-consumer-secret>'
key = '<your-api-key-riot>'

ids = []
lastGames = []
names = [<list-of-summoner-names>]
ru = RiotWatcher(key, default_region=RUSSIA)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
print('Bot started')
for name in names:
    sumId = ru.get_summoner(name)['id']
    ids.append(sumId)
    lastGame = ru.get_recent_games(sumId)['games'][0]['gameId']
    lastGames.append(lastGame)
    sleep(1)

while(1):
    try:
        for i in range(0,len(ids)):
            lastGame = ru.get_recent_games(ids[i])['games'][0]
            if lastGame['gameId'] <> lastGames[i]:
                lastGames[i] = lastGame['gameId']
                mode = lastGame['subType'].lower().replace('_', ' ')
                stats = lastGame['stats']
                ended = 'won' if stats['win'] else 'lost'
                seconds = stats['timePlayed']
                m, s = divmod(seconds, 60)
                tweet = ("%s %s %s with %i/%i/%i in %i:%02i" % (names[i], ended, mode, stats['championsKilled'], stats['numDeaths'], stats['assists'],m,s))
                print('%i %s'%(lastGame['gameId'], tweet))
                api.update_status(tweet)
                sleep(1)
    except LoLException:
        sleep(10)
    sleep(20)