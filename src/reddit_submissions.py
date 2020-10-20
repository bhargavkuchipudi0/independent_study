from datetime import datetime
import time
import json
import requests
import math
import os
import sys
import csv

cwd = os.getcwd().split('/')
cwd.pop()
path = '/'.join(cwd) + '/reddit_results/' # directory for all the results.

post_id = dict() # Stores all posts ID's to eliminate duplicate data.
sub_reddits = ['parenting', 'babybumps', 'beyondthebump'] # Sub Reddits.
query_terms = ['covid-19','coronavirus', 'corona', 'covid', 'sars-cov-2', '2019-nCoV', 'birth interventions', 'home birth', 'induced', 'flu shot', 'tdap', 'vaccination', 'vaccine'] # Query Terms.
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'novembers', 'december']

query_count_by_month = dict() # Count the number of posts from each sub_reddit and each query term by month

for query in query_terms:
    query_count_by_month[query] = dict()
    for month in months:
        query_count_by_month[query][month] = [0 for i in sub_reddits]

query_count = dict()
for query in query_terms:
    query_count[query] = [0 for i in sub_reddits]


class RedditSubmisions:

    def __init__(self, start_date, end_date):
        self.start_date = math.floor(time.mktime(datetime.strptime(start_date, "%d/%m/%Y").timetuple()))
        self.end_date = math.floor(time.mktime(datetime.strptime(end_date, "%d/%m/%Y").timetuple()))
        self.payload = {
            'q': '',
            'after': '',
            'before': '',
            'subreddit': ''
        }

    def getRedditSubmissions(self, payload):
        url = 'https://api.pushshift.io/reddit/submission/search/'
        try:
            print('Getting data from: {0} to: {1} [q: {2}, subreddit: {3}]'.format(datetime.fromtimestamp(int(payload['after'])).strftime('%Y-%m-%d'), datetime.fromtimestamp(int(payload['before'])).strftime('%Y-%m-%d'), payload['q'], payload['subreddit']))
            response = requests.get(url, params = payload)
            if (response.status_code == 200):
                json_response = response.json()
                if (len(json_response['data']) > 0):
                    return True, json_response
                else:
                    return True, None
            else:
                return True, None
        except Exception as error:
            print(error)
            return False, error

def update_query_count(sub_reddit, query_term, data):
    query_count[query_term][sub_reddit] += len(data) # not considering the duplicate posts.
    

def writeDataToCsv(writer, data, count, sub_reddit, query_term):
    data = filterData(data)
    for d in data:
        # if count == 1:                # |
        #     header = d.keys()         # | Uncomment these lines to write the posts on a csv file
        #     writer.writerow(header)   # |
        # writer.writerow(d.values())   # |
        
        # query_count_by_month[query_term][months[int(d['created_utc'].split('-')[1])-1]][sub_reddit] += 1 # increment the count of the post by month
        query_count[query_term][sub_reddit] += 1 # Increment the count 
        

def filterData(data):
    new_data = []
    for d in data:
        if (d['id'] in post_id): continue
        else: post_id[d['id']] = 1
        obj = dict()
        obj['id'] = d['id'] if 'id' in d else None
        obj['created_utc'] = datetime.fromtimestamp(int(d['created_utc'])).strftime('%Y-%m-%d') if 'created_utc' in d else None
        obj['author'] = d['author'] if 'author' in d else None
        obj['title'] = d['title'] if 'title' in d else None
        obj['selftext'] = d['selftext'] if 'selftext' in d else None
        obj['num_comments'] = d['num_comments'] if 'num_comments' in d else None
        obj['num_crossposts'] = d['num_crossposts'] if 'num_crossposts' in d else None
        obj['score'] = d['score'] if 'score' in d else None
        obj['subreddit'] = d['subreddit'] if 'subreddit' in d else None
        obj['total_awards_received'] = d['total_awards_received'] if 'total_awards_received' in d else None
        obj['upvote_ratio'] = d['upvote_ratio'] if 'upvote_ratio' in d else None
        new_data.append(obj)

    
    return new_data


def createFolder(path): 
    if not os.path.exists(path):
        os.makedirs(path)


def getCsvFileWriter(path):
    data_file = open(path, 'w')
    return data_file, csv.writer(data_file)


def writeCountToCSV():
    file = path + 'reddit_submissions_count.csv'
    f, csv_writer = getCsvFileWriter(file)
    csv_writer.writerow(['query terms']+sub_reddits)
    for key in query_count:
        csv_writer.writerow([key] + query_count[key])
    f.close()


def main(start_date, end_date):
    # week_timestamp = 60 * 60 * 24 * 7 # 1 Week time stamp
    day_timestamp = 60 * 60 * 25 # 1 Day time stamp
    reddit = RedditSubmisions(start_date, end_date)
    global path
    createFolder(path)
    file = path + 'reddit_submissions.csv'
    f, csv_writer = getCsvFileWriter(file)
    count = 0
    for i, sub in enumerate(sub_reddits):

        reddit.payload['subreddit'] = sub
        for term in query_terms:
            reddit.payload['q'] = term
            after_time = reddit.start_date
            before_time = reddit.start_date + day_timestamp

            while (before_time <= reddit.end_date):
                reddit.payload['after'] = str(after_time)
                reddit.payload['before'] = str(before_time)
                status, res = reddit.getRedditSubmissions(reddit.payload)
                if status and res:
                    count += 1
                    # writeDataToCsv(csv_writer, res['data'], count, i, term)
                    update_query_count(i, term, res['data'])
                elif not status:
                    f.close()
                    sys.exit()
                time.sleep(0.5)
                after_time = before_time - (60 * 60 * 1)
                if (before_time == reddit.end_date): 
                    break
                before_time += day_timestamp
                if (before_time > reddit.end_date):
                    before_time = reddit.end_date
    f.close()
    writeCountToCSV()
    print(query_count)
    

if __name__ == '__main__':
    start_date = '01/01/2020' # DD/MM/YYYY (01 JAN 2020)
    end_date = '01/10/2020'   # DD/MM/YYYY (01 OCT 2020)
    main(start_date, end_date) 
    sys.exit()
    
