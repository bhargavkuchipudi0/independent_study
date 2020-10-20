from datetime import datetime
import requests
import math
import time

payload = {
    'after': '',
    'before': '',
    'limit': 100,
    'subreddit': '',
    'sort_type': 'score',
    'sort': 'desc'
}

start_date = '01/01/2020' # DDMMYYY (01 JAN 2020).
unix_start_date = math.floor(time.mktime(datetime.strptime(start_date, "%d/%m/%Y").timetuple())) # UNIX time stamp.
end_date = '01/10/2020' # DDMMYYY (01 OCT 2020).
unix_end_date = math.floor(time.mktime(datetime.strptime(end_date, "%d/%m/%Y").timetuple())) # UNIX time stamp.
half_day = 12 * 60 * 60 # Half day in seconds.
sub_reddits = ['parenting', 'babybumps', 'beyondthebump']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'novembers', 'december']
monthly_posts = {
    'january': [0, 0, 0],  # [parenting, babybumps, beyondthebump]
    'february': [0, 0, 0],
    'march': [0, 0, 0],
    'april': [0, 0, 0],
    'may': [0, 0, 0],
    'june': [0, 0, 0],
    'july': [0, 0, 0],
    'august': [0, 0, 0],
    'september': [0, 0, 0],
    'october': [0, 0, 0],
    'novembers': [0, 0, 0],
    'december': [0, 0, 0],
}

def postCount():
    url = 'https://api.pushshift.io/reddit/submission/search/'

    for i, sub in enumerate(sub_reddits):
        after = unix_start_date
        before = after + half_day
        payload['subreddit'] = sub
        while after < unix_end_date:
            payload['after'] = after
            payload['before'] = before
            response = requests.get(url, params = payload)
            if (response.status_code == 200):
                json_res = response.json()
                month = months[int(datetime.fromtimestamp(int(after)).strftime('%d-%m-%Y').split('-')[1])-1]
                monthly_posts[month][i] += len(json_res['data'])
                after += half_day
                before += half_day
                # time.sleep(1)
        print(monthly_posts)



if __name__ == '__main__':
    postCount()