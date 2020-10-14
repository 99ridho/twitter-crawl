from http_client import (HTTPClient, HTTPRequestData)
from typing import (Optional, Any, Dict, List)
from config import BEARER_TOKEN

class TweetSearchData:
    def __init__(self, id: str, text: str):
        self.id = id
        self.text = text

    def __repr__(self):
        return f'TweetSearchData(id = {self.id}, text = {self.text})'

class TwitterService:
    def __init__(self):
        self.http_client = HTTPClient()
        self.bearer_token = BEARER_TOKEN

    async def get_recent_tweet_search(self, query: str) -> Optional[List[TweetSearchData]]:
        params: Dict[str, any] = {
            'query': query,
            'max_results': 100
        }

        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.bearer_token}'         
        }

        request_data = HTTPRequestData(
            'https://api.twitter.com/2',
            path='/tweets/search/recent',
            method='GET',
            params=params,
            headers=headers
        )

        json = await self.http_client.request(request_data)

        if json is None:
            return None

        tweets = set(map(lambda raw_tweet: TweetSearchData(id=raw_tweet['id'], text=raw_tweet['text']), json['data']))

        return tweets
