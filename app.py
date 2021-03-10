import requests
from flask import Flask, render_template, session, redirect, request, url_for, g

from database import Database
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from user import User

app = Flask(__name__)
app.secret_key = '1234'

Database.initialise(database='learning', host='localhost', user='postgres', password='DJ%WFbULyuXnTLh8GD9H%Vn&D4PA')


@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_from_db_by_screen_name(session['screen_name'])


@app.route('/')  # http://127.0.0.1:4495/
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')  # 1. Send user to Twitter
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    request_token = get_request_token()
    session[
        'request_token'] = request_token  # Persistent between requests; leaving and coming back the request token is preserved

    return redirect(get_oauth_verifier_url(request_token))  # 2. User verifies themselves with Twitter


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route(
    '/auth/twitter')  # http://127.0.0.1:4995/auth/twitter?oauth_verifier=156454  || 3. The user comes back with oauth_verifier
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')  # Get oauth_verifier
    access_token = get_access_token(session['request_token'],
                                    oauth_verifier)  # 4. Use oauth_verifier and request token to generate an access token

    user = User.load_from_db_by_screen_name(access_token['screen_name'])  # 5. Load the user by screen_name

    if not user:  # 6. If they don't exist then we create a new User to save to the database
        user = User(None, access_token['screen_name'], access_token['oauth_token'],
                    access_token['oauth_token_secret'])
        user.save_to_db()

    session['screen_name'] = user.screen_name  # 7. Set the screen_name for the session

    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)


@app.route('/search')
def search():
    user_query = request.args.get('q')
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(user_query))

    tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']]

    for tweet in tweet_texts:
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label

    return render_template('search.html', content=tweet_texts)


app.run(port=4995, debug=True)
