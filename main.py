from twitter_search_service import TwitterSearchService
from asyncio import (get_event_loop)

async def main():
    svc = TwitterSearchService()
    tweets = await svc.get_recent_tweet_search('omnibus law')
    for tweet in tweets:
        print(tweet)

loop = get_event_loop()
loop.run_until_complete(main())