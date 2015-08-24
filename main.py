from songkick import Songkick
from concertbot import ConcertBot
import time

queries = ["!cb", "Paul McCartney", "Childish Gambino", "childsh Gambino", "blink 182", "wafafaa", "P/'daa", "gorillaz", "dream theater", "Michael Jackson", "cher", ""]

cb = ConcertBot("sampleuser", "samplepass", 'sample_api_key')

def testQueries():
    for i in queries:
        cb.call_Songkick(i,"cheese")
        time.sleep(2)

def calendar_lookup():
    pass

cb.login()
cb.run_bot()