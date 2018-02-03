from steem import Steem
from steembase import exceptions
import time
import datetime

identifier = []

# Steemit API Node
nodes = ["https://api.steemit.com"]

#your account name
account = "wil1liam"

# private posting key | private active key (to log in)
keys=["private posting key", "private active key"]

s = Steem(nodes,keys=keys)

def relike(account):

    # your newest post
    post_identifier = get_newest_post(account)

    #the people who liked your post
    usernames = get_voter(post_identifier)

    # the newest posts of the people who liked your post + upvote their posts
    upvote_newest_post(usernames,account)

def get_newest_post(username):
    newest_post = s.get_discussions_by_blog({"limit":1,"tag":username})
    if(newest_post!=[]):
        return newest_post[0]["author"]+"/"+newest_post[0]["permlink"]
    else:
        return None



def get_voter(post_identifier):
    post_identifier = post_identifier.split("/")
    votes = s.get_active_votes(post_identifier[0],post_identifier[1])
    voter = []
    for i in votes:
        if (i["voter"] != post_identifier[0]):
            voter.append(i["voter"])
    return voter

def upvote_newest_post(usernames,default_account):
    for i in usernames:
        if (i!=account):
            upvote_post = get_newest_post(i)
        try:
            s.commit.vote(identifier=upvote_post, weight=100, account=default_account)
            
        except exceptions.RPCError:
            pass


while (1):
    print("\n",time.ctime())
    relike(account)
    time.sleep(5*60)
