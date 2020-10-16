from http_client import (HTTPClient, HTTPRequestData)
from typing import (Optional, Any, Dict, List)
from config import BEARER_TOKEN
from urllib.parse import parse_qsl
import asyncio
import json

class TweetSearchResponse:
    def __init__(self, data: List[str], next_token: str):
        self.data = data
        self.next_token = next_token

    def __repr__(self):
        return f'Response(data = {self.data}, next_token = {self.next_token})'

class TwitterSearchService:
    def __init__(self, query: str, max_item_count: int):
        self.http_client = HTTPClient()
        self.bearer_token = BEARER_TOKEN
        self.next_token = ''
        self.query = query
        self.max_item_count = max_item_count
        self.__lock = asyncio.Lock()

    def __make_search_data(self, tweet: Any) -> str:
        text = tweet['text']

        if 'extended_tweet' in tweet:
            text = tweet['extended_tweet']['full_text']
        elif 'retweeted_status' in tweet:
            text = tweet['retweeted_status']['text']
            if 'extended_tweet' in tweet['retweeted_status']:
                text = tweet['retweeted_status']['extended_tweet']['full_text']

        return text

    async def __get_recent_tweet_search(self, params: Dict[str, any]) -> Optional[TweetSearchResponse]:
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.bearer_token}'         
        }

        request_data = HTTPRequestData(
            'https://api.twitter.com/1.1',
            path='/tweets/search/30day/dev.json',
            method='GET',
            params=params,
            headers=headers
        )

        json = await self.http_client.request(request_data)
        if json is None:
            return None

        if 'next' not in json:
            return None

        self.next_token = json['next']
        
        tweets = []
        tweets_temp = list(map(self.__make_search_data, json['results']))

        for t in tweets_temp:
            if t not in tweets:
                tweets.append(t)

        return TweetSearchResponse(data=tweets, next_token=self.next_token)

    async def get_next_results(self) -> Optional[TweetSearchResponse]:
        async with self.__lock:
            param = {
                'query': f'\"{self.query}\" lang:id',
                'maxResults': self.max_item_count
            }

            if self.next_token:
                param['next'] = self.next_token

            return await self.__get_recent_tweet_search(param)