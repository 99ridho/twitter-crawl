from http_client import (HTTPClient, HTTPRequestData)
from typing import (Optional, Any, Dict, List)
from config import BEARER_TOKEN

class TweetSearchData:
    def __init__(self, id: str, text: str, type: str):
        self.id = id
        self.text = text
        self.type = type

    def __repr__(self):
        return f'TweetSearchData(id = {self.id}, text = {self.text}, type = {self.type})'

class TwitterSearchService:
    def __init__(self):
        self.http_client = HTTPClient()
        self.bearer_token = BEARER_TOKEN

    def __make_search_data(self, tweet: Any) -> TweetSearchData:
        return TweetSearchData(
            id=tweet['id_str'],
            text=tweet['full_text'],
            type=tweet['metadata']['result_type']
        )

    async def get_recent_tweet_search(self, query: str) -> Optional[List[TweetSearchData]]:
        params: Dict[str, any] = {
            'q': f'{query} -filter:retweets',
            'count': 100,
            'include_entities': 'false',
            'tweet_mode': 'extended',
            'result_type': 'mixed'
        }

        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.bearer_token}'         
        }

        request_data = HTTPRequestData(
            'https://api.twitter.com/1.1',
            path='/search/tweets.json',
            method='GET',
            params=params,
            headers=headers
        )

        json = await self.http_client.request(request_data)

        if json is None:
            return None

        tweets = set(map(self.__make_search_data, json['statuses']))

        return tweets
