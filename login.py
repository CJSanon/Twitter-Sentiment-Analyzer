import constants
import oauth2
import urllib.parse as urlparse

from database import Database
from user import User
from twitter_utils import consumer, get_request_token, get_oauth_verifier, get_access_token

Database.initialise(database='learning', host='localhost', user='postgres', password='DJ%WFbULyuXnTLh8GD9H%Vn&D4PA')

user_screen_name = input("What is your screen name? ")

user = User.load_from_db_by_screen_name(user_screen_name)

if not user:
    request_token = get_request_token()

    # Store the pin code
    oauth_verifier = get_oauth_verifier()

    access_token = get_access_token(request_token, oauth_verifier)

    user = User(None, user_screen_name, access_token['oauth_token'], access_token['oauth_token_secret'])
    user.save_to_db()

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images',
                              'GET')  # Loads the string and converts into a Python dictionary

for tweet in tweets['statuses']:
    print(tweet['text'])

#  www.ourwebsite.com "log in with twitter button"
# they press "Sign In" or "authorize" in Twitter.com
# Twitter sends them back to our website with /auth
# We get that auth code + request token -> twitter -> access token
