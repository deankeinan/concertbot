__author__ = 'DKeinan'
import logging
from sqlmanager import SQLManager
from songkick import Songkick, ArtistResponseObject, EventResponseObject
import praw
import traceback
import time
logging.basicConfig(filename='testing.log', filemode='w', format='%(message)s',level=logging.INFO)

USERAGENT = "Dean Keinan's concert information bot"
SUBREDDIT = "concertbot"
PARENTSTRING = ["!cb", "!concertbot", "!livemusic"]
SIGNATURE = "\n\n^*I'm&nbsp;a&nbsp;bot&nbsp;powered&nbsp;by&nbsp;SongKick,&nbsp;and&nbsp;I&nbsp;dig&nbsp;live&nbsp;music.&nbsp;[Why?](http://deankeinan.com/concertbot)*"
BAD_INPUT = "Hey there! I couldn't understand what you said.\n\nYou can call me by saying:\n\n !cb \"*Artist Name*\""
NO_RESULTS = "Oops! I couldn't find any artists by that name. I'll keep an eye out for them.\n\n"
MAXPOSTS = 6
WAIT = 20

class ConcertBot(object):

    """A Reddit bot that scans for mentions and delivers information on concerts. A ConcertBot has the following properties:

    Attributes:
        username: The username of the Reddit account being logged into.
        password: The password of the Reddit account being logged into.
        sk_key: A valid Songkick API.
        reply_string: The string containing the response to a found comment.
        query: The string containing the payload for a Songkick API request.
        db: An instance of SQLManager to manage a database of posts already replied to.
        r: An instance of the PRAW wrapper to manage Reddit API actions.
        sk: An instance of Songkick to manage Songkick API actions.

    Constants:
        USERAGENT: A short description of what the bot does
        SUBREDDIT: The sub or list of subs to be scanned for new posts.
        PARENTSTRING: The keywords we're looking for
        MAXPOSTS: The maximum number of posts responded to per run.
        WAIT: The time (in seconds) to wait in between runs.
        BAD_INPUT: A premade error message to reply.
        SIGNATURE: A line of text found at the end of every post

    Methods:
        init: Class takes username and password values and initializes a sql database and reddit client using PRAW.
        login: Logs into Reddit using the credentials stored in the instance variables.
    """

    def __init__(self, username, password, sk_key):
        self.reply_string = ""
        self.username = username
        self.password = password
        self.query = ""
        self.db = SQLManager()
        self.r = praw.Reddit(USERAGENT)
        self.sk = Songkick(sk_key)

    def login(self):
        logging.info('BOT: Logging in...')
        self.r.login(self.username, self.password)

    def search_for_posts(self):

        logging.info('BOT: Searching /r/'+ SUBREDDIT + '.')

        subreddit = self.r.get_subreddit(SUBREDDIT)
        posts = subreddit.get_comments(limit=MAXPOSTS)

        for post in posts:
            pid = post.id

            try:
                pauthor = post.author.name
                logging.info("Looking at post %s", pid)
                self.db.select_by_postID(pid)

                if not self.db.fetch_selection(): #If the current post isn't found in the database of old posts
                    pbody = post.body

                    if any(key in pbody for key in PARENTSTRING):
                        logging.info('BOT: Found a key match.')
                        if pauthor.lower() != self.username.lower():
                            #Split comment text by quotes to catch payload
                            catch = pbody.split('"')

                            if not catch: #Empty payload
                                self.send_reply(BAD_INPUT, post)

                            else: #Send payload to Songkick
                                self.call_Songkick(catch[1], post)
                        else:
                            #Current post author account matches bot username.
                            logging.info('BOT: Will not reply to self account.')
                            self.db.insert_oldpost(pid)
                    else:
                        pass

            except AttributeError:
                #Author is deleted. We don't care about this.
                logging.info("Post %s deleted.", pid)
                pass

    def send_reply(self,content,recipient):
        logging.info('BOT: Replying to ' + recipient.id + ' by ' + recipient.author.name + '.')
        logging.info("BOT: ********")
        logging.info("%s",content)
        logging.info("BOT: ********")
        recipient.reply(content + SIGNATURE)
        self.db.insert_oldpost(recipient.id)
        self.reply_string = ""

    def call_Songkick(self, payload, current_post):
        try:
            artist = self.sk.get_artist_info_by_name(payload)
        except ValueError:
            self.send_reply(BAD_INPUT, current_post)
            return None
        if not artist:
            self.send_reply(NO_RESULTS, current_post)
            return None


        #Find upcoming events
        try:
            calendar = self.sk.get_events_by_artistID(artist.id)
        except ValueError:
            self.send_reply(BAD_INPUT, current_post)
            return None
        if not calendar:
            self.send_reply("Couldn't find any upcoming tour dates for ["+artist.name+"](" + artist.url + "). Laaaame.\n\n", current_post)
            return None
        else:
            #begin building reply
            self.reply_string = "Hey there! Here's where " + artist.name + " will be performing soon:"
            #list the events and their dates
            for i in calendar.list_events[:6]:
                datesplit = i["start"]["date"].split('-')
                self.reply_string += "\n\n* " + datesplit[1] +"/"+ datesplit[2] + " @ " + i["location"]["city"]
            #append with link to songkick page
            if calendar.num_events > 6:
                self.reply_string += "\n\n" + str((calendar.num_events - 6)) + " events not shown. Click [here](" + artist.url + ") to view or buy tickets."
                self.send_reply(self.reply_string,current_post)
                return None
            else:
                self.reply_string += "\n\nClick [here](" + artist.url + ") to view more information or buy tickets."
                self.send_reply(self.reply_string,current_post)
                return None


    def run_bot(self):
        while True:
            try:
                self.search_for_posts()
            except Exception as e:
                traceback.print_exc()
            print('Running again in %d seconds \n' % WAIT)
            time.sleep(WAIT)
