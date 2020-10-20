from urllib.request import urlopen
import simplejson
import time

# #    print p
# _char_map = {8722: '-', 8211: '-', 8212: '-', 8213: '-', 8216: "'", 8217: "'", 8218: ',', 8220: '"', 8221: '"', 8230: '...', 187: '>>', 7789: 't', 171: '<<', 173: '-', 180: "'", 699: "'", 7871: 'e', 192: 'A', 193: 'A', 194: 'A', 195: 'A', 196: 'A', 197: 'A', 198: 'Ae', 199: 'C', 200: 'E', 201: 'E', 202: 'E', 203: 'E', 204: 'I', 7885: 'o', 206: 'I', 205: 'I', 208: 'D', 209: 'N', 210: 'O', 211: 'O', 212: 'O', 213: 'O', 214: 'O', 215: 'x', 216: 'O', 217: 'U', 218: 'U', 207: 'I', 220: 'U', 221: 'Y', 223: 'S', 224: 'a', 225: 'a', 226: 'a', 227: 'a', 228: 'a', 229: 'a', 230: 'ae', 231: 'c', 232: 'e', 233: 'e', 234: 'e', 235: 'e', 236: 'i', 237: 'i', 238: 'i', 239: 'i', 240: 'o', 241: 'n', 242: 'o', 243: 'o', 244: 'o', 245: 'o', 246: 'o', 247: '/', 248: 'o', 249: 'u', 250: 'u', 251: 'u', 252: 'u', 253: 'y', 255: 'y', 256: 'A', 257: 'a', 259: 'a', 261: 'a', 263: 'c', 268: 'C', 269: 'c', 279: 'e', 281: 'e', 283: 'e', 287: 'g', 219: 'U', 298: 'I', 299: 'i', 304: 'I', 305: 'i', 322: 'l', 324: 'n', 332: 'O', 333: 'o', 335: 't', 337: 'o', 339: 'oe', 345: 'r', 346: 'S', 347: 's', 351: 's', 352: 'S', 353: 's', 355: 'c', 363: 'u', 367: 'u', 378: 'z', 379: 'Z', 381: 'Z', 382: 'z', 924: 'M', 451: '!'}
# def toascii(text):
#     if type(text) is not str:
#         try:
#             text = str(text, "utf-8", 'ignore')
#         except TypeError as e:
#             pass
#         text = unicodedata.normalize('NFKD', text)
#     ret = [c if ord(c) < 128 else _char_map.get(ord(c), '') for c in text]
#     ret = ''.join(ret)
#     return ret  


lsSubs = ['parenting','babybumps','beyondthebump']
lsTerms = ['covid','corona', 'coronavirus', 'sars-cov-2', 'covid-19', '2019-nCoV']

for sub in lsSubs:
    for term in lsTerms:
        #JAN_1_2020
        unix_timestamp = 1577836800
        amt = (60*60*24*7) #one week
        week_after = unix_timestamp + amt
        
        
        for i in range(1,(52) + 1): #1 years
            f = open('reddit_results/' + term + sub + str(i) + '.txt','w+')
            print('WEEK ' + str(i))
            request = 'https://api.pushshift.io/reddit/submission/search/?q='+term + '&after=' + str(unix_timestamp) + '&before=' + str(week_after) + '&subreddit=' + sub

            try:    
                resultDict = simplejson.loads(urlopen(request).read())
                #print(resultDict)
                
                f.write(simplejson.dumps(resultDict))
              
                unix_timestamp = unix_timestamp + amt
                week_after =  week_after + amt
                time.sleep(2) #sleep a bit to not get timeouts
                f.close()
            except Exception as ex:
                print(ex)
                f.close()
                assert(0)


        
    
    
