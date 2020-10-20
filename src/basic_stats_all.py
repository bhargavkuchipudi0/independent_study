from urllib.request import urlopen
import simplejson
import time
from datetime import datetime

unix_timestamp = 1601510400 #October 1, 2020
#amt = (60*60*24*7) #one week
amt = (60*60*12) #1 days
half_month_before = unix_timestamp - amt

f = open('all_20_beyondthebump.txt','w')
for i in range(1,(280*2) + 1):
    # print('HALF DAY ' + str(i))
    request = 'https://api.pushshift.io/reddit/submission/search/?size=1200&after=' + str(half_month_before) + '&before=' + str(unix_timestamp) + '&sort_type=score&sort=desc&subreddit=beyondthebump'
    # print(request)
    #print request2
    try:
        json = simplejson.loads(urlopen(request).read()) 
        json = json['data']
        num_comments = 0
        if len(json) > 0:
            num_comments = len(json)
            # print(str(num_comments))
            f.write(datetime.fromtimestamp(int(half_month_before)).strftime('%Y-%m-%d') + '--' + datetime.fromtimestamp(int(unix_timestamp)).strftime('%Y-%m-%d') + ' ' + str(num_comments)+'\n')
        else:
            f.write('0\n')
      
        unix_timestamp = unix_timestamp - amt
        half_month_before = half_month_before - amt
        time.sleep(0.5) #sleep a bit to not get timeouts
    except Exception as ex:
        print(ex)
        f.close()
        assert(0)


f.close()
    
    
