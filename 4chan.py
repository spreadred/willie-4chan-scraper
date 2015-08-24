'''
Created on Feb 16, 2014

@author: Rohn
'''
import json
import time
import urllib2
import willie
from HTMLParser import HTMLParser
from operator import itemgetter


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

@willie.module.commands("4chan")
def execute4Chan(bot, trigger):
    if trigger.owner:
        chan_scrape(bot, trigger)    

def chan_scrape(bot, trigger, board, minutes):
    sorted_threads = getPopularThreads()
    
    bot.say("Top 5 threads on 4chan /b/ in the past 30 minutes")          
    for x in range(0,5):
        if sorted_threads[x].has_key('com') and sorted_threads[x].has_key('no'):
            bot.say(strip_tags(sorted_threads[x]['com'][:80].decode('unicode_escape'.encode('ascii', 'ignore'))) + "... [http://boards.4chan.org/b/res/" + str(sorted_threads[x]['no']) + "]")

def isValidBoard(board):
    '''
    "boards": [
        {
            "board": "3",
            "title": "3DCG",
            "ws_board": 1,
            "per_page": 15,
            "pages": 11
        },
    '''
    
    boardsJSON = urllib2.urlopen("http://a.4cdn.org/boards.json")
    
# use 4chan json to get <number> most popular threads from <board> in the past <minutes>          
def getPopularThreads(board, minutes, number): 

    theJSON = urllib2.urlopen("http://a.4cdn.org/b/catalog.json")

    pages = json.load(theJSON)
    
    threadsList = []
    
    for page in pages:
        for thread in page['threads']:
            # we only want threads with replies in the last 30 minutes
            if thread['time'] >= time.time() - 1800:
                threadsList.append(thread)
      
    # sort the list, grab top ten
    sorted_threads = sorted(threadsList, key=itemgetter('replies'), reverse=True)
    
    return sorted_threads
