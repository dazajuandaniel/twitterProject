#http://www.kalisch.biz/2013/10/harvesting-twitter-with-python/
#Library Imports
import tweepy as tw
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key = 'XqNOFK3tkWO3ueraq4WJgAbL8'
consumer_secret = 'KA79XONJOZL8WkBpZAuqkTjDxRhiT7KGf16x2SLTCFfqSpTnoG'
access_token = '140966719-NrfyS8phWv3pJAwCQkqoZESAWTQo6AQzfVVYH1Rf'
access_secret = 'Efi3AuiHq1DTIAfucEFt7SgCZ8rFHsF4Cibk1RJNC95Rt'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth)

#Coordinates for Tweet filter
victoria = [141.157913, -38.022041, 146.255569, -36.412349]
nsw = [149.419632, -34.551717, 151.880570, -32.768704]

class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        db.save(tweet)
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = StdOutListener()
    stream = Stream(auth,listener)

    #stream.filter(track=['python', 'javascript', 'ruby'])
    stream.filter(locations=victoria)

