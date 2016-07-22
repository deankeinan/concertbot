# concertbot

##The solution for music loving Reddit users that isn't quite a solution yet.

Another simple idea: post a comment on Reddit about a music artist, and receive a response that looks like the image below. Hosted on a DigitalOcean droplet, it uses a fresh python script and the SongKick API to make the magic happen.

Right now, it's dysfunctional because I haven't updated it to comply with Reddit's OAuth policy for bots yet, but the core mechanism still works fine. There's still quite a bit where I want this to go.

Ideally, the script would crawl /r/music & /r/listentothis looking for top or controversial posts, and autonomously comment providing information about the artist. Problem is, typically what's posted on those subreddits are youtube links, which have different title schemes depending on who posted them, and the SongKick artist lookup is pretty sensitive. 

(Last thing we wanna do is post info about the wrong artist (*how embarassing*.) There might be a way around this using YouTube's API. In certain videos I think they’re IDing music and suggesting it as a purchase, so maybe that info is accessible.

For the future, I imagine concertbot providing links to videos of that artist performing live, maybe play a role in a larger standalone web page that serves a similar purpose.

Hmm...
