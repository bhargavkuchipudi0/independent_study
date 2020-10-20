from datetime import datetime
import time
import json
import requests
import math
import os
import sys
import csv

token = '' # oauth token 
token_time = 0 # Time stamp of token accessed before
sub_reddits = ['parenting', 'babybumps', 'beyondthebump'] # Sub Reddits.
query_terms = ['covid-19','coronavirus', 'corona', 'covid', 'sars-cov-2', '2019-nCoV', 'birth interventions', 'home birth', 'induced', 'flu shot', 'tdap', 'vaccination', 'vaccine'] # Query Terms.
path = ''


def access_oauth_token():
    global token, token_time
    client_auth = requests.auth.HTTPBasicAuth('PVVlwB0vkQ1jfg', 'VPnxQ7KiuCzOFDgKo-z4x4BZI5U')
    post_data = {"grant_type": "password", "username": "bhargav0286", "password": "Bhargavsatya0286#"}
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    response = response.json()
    token = response['access_token']
    token_time = math.ceil(time.time())
    print(token)

def get_path():
    global path
    cwd = os.getcwd().split('/')
    cwd.pop()
    path = '/'.join(cwd) + '/reddit_results'


def search_subreddit(subreddit, q, after):
    headers = {"Authorization": "bearer " + token, "User-Agent": "reddit bhargav0286"}
    payload = {
        'subreddit': subreddit,
        'q': q,
        'after': after,
    }
    try:
        response = requests.get("https://oauth.reddit.com/subreddits/search", headers = headers, params=payload)
        return response.json() if response.status_code == 200 else response.status_code
    except Exception as error:
        print(error)
        sys.exit()


def process_data(response):
    print(len(response['data']['children']))
    for obj in response['data']['children']:
        curr = obj['data']
        print(curr['id'], curr['created_utc'])

def get_data(start_date, end_date):
    start_date = math.floor(time.mktime(datetime.strptime(start_date, "%m/%d/%Y").timetuple())) # converting date to unix time stamp.
    end_date = math.floor(time.mktime(datetime.strptime(end_date, "%m/%d/%Y").timetuple())) # converting date to unix time stamp.
    one_day_ts = 60 * 60 * 24 # unix time stamp of a day.

    for _, sub in enumerate(sub_reddits):
        for _, q in enumerate(query_terms):
            after = ''

            while (before <= end_date):
                response = search_subreddit(sub, q, after)
                if response:
                    process_data(response)
                else:
                    print('something went wrong with status_code:{0}'.format(response))
                    sys.exit()
                time.sleep(2)



def main(start_date, end_date):
    access_oauth_token()
    get_data(start_date, end_date)


if __name__ == '__main__':
    get_path()
    main('01/01/2020', '10/01/2020') # MMDDYYYY
