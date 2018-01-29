from steem import Steem
from steembase import exceptions

# Steemit API Node
nodes = ["https://api.steemit.com"]

#your account name
account = "wil1liam"

# private posting key | private active key (to log in)
keys=["private posting key", "private active key"]

def relike(account,keys,nodes):

    def newest_post(username):
        limit = 100
        result = None
        while (result==None):
            account_history = s.get_account_history(username,index_from=-1,limit=limit)
            try:
                for i in range(limit+1):
                    operation = account_history[limit-i]
                    if (operation[1]["op"][0] == "comment"):
                        if (operation[1]["op"][1]["title"]!= ""):
                            result = operation[1]["op"][1]["permlink"]
                            return result
            except IndexError:
                return None
            limit = limit * 2
        return result


    s = Steem(nodes,keys=keys)

    post_1 = newest_post(username=account)
    #post_1 = "the-classic-meme-zg1hbmlh-ze3wl" pls upvote if you see this :)
    votes = s.get_active_votes(account,post_1)

    voter = []


    for i in range(len(votes)):
        if (votes[i]["voter"] != account):
            voter.append(votes[i]["voter"])


    suc_voter_count = 0
    nopost_found = 0
    #upvote a post
    for i in range(len(voter)):
        post_2 = newest_post(username=voter[i])

        if (post_2!=None):
            upvote_post = voter[i]+"/"+post_2
            try:
                s.commit.vote(identifier=upvote_post, weight=100, account=account)
                suc_voter_count += 1
            except exceptions.RPCError:
                pass
        else:
            nopost_found +=1

    log = "No post found for "+str(nopost_found)+"/"+str(len(voter))+" users\nsuccessfully voted for "+str(suc_voter_count)+"/"+str(len(voter))+" users.\n"
    return log

print(relike(account=account,keys=keys,nodes=nodes))
