from twitter_service import TwitterService
from asyncio import (get_event_loop)

async def main():
    svc = TwitterService()
    tweets = await svc.get_recent_tweet_search('omnibus law')
    for tweet in tweets:
        print(tweet)

loop = get_event_loop()
loop.run_until_complete(main())