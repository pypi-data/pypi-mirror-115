"""MIT License

Copyright (c) 2021 gunyu1019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
import logging
import aiohttp
import asyncio

from typing import List

from .https import HttpClient
from .enums import WebsiteType
from .models import *
from .errors import ClientException, TooManyRequests

log = logging.getLogger(__name__)


class Client:
    """ discord.py 에 있는 `discord.Client`를 기반으로 한 KoreanBots 클라이언트, top.gg 클라이언트, UniqueBots 클라이언트에 연결됩니다.
    이 클래스를 통하여 KoreanBots API와 top.gg API, UniqueBots API에 연결됩니다.

    일부 옵션은 `discord.Client`를 통하여 전달될 수 있습니다.

    Parameters
    ----------
    bot: discord.Client
        discord.py의 클라이언트입니다.
        Client 대신 `AutoShardedClient`, `Bot`, `AutoShardedBot`를 넣을 수도 있습니다.
    koreanbots_token: Optional[str]
        Koreanbots 에서 발급받은 봇의 토큰 키값 입니다. 해당 값을 설정하지 않을 경우 자동으로 활성화 되지 않습니다.
    topgg_token: Optional[str]
        Top.gg 에서 발급받은 봇의 토큰 키값 입니다. 해당 값을 설정하지 않을 경우 자동으로 활성화 되지 않습니다.
    uniquebots_token: Optional[str]
        UniqueBots 에서 발급받은 봇의 토큰 키값 입니다. 해당 값을 설정하지 않을 경우 자동으로 활성화 되지 않습니다.
    session: Optional[aiohttp.ClientSession]
        HttpClient 를 위한 aiohttp 의 ClientSession 클래스 입니다.
        기본값은 None이며, 자동으로 ClientSession을 생성하게 됩니다.
    loop: Optional[asyncio.AbstractEventLoop]
        비동기를 사용하기 위한 asyncio.AbstractEventLoop 입니다.
        기본값은 None이거나 bot 오브젝트가 들어왔을 때에는 bot.loop 입니다.
        기본 asyncio.AbstractEventLoop는 asyncio.get_event_loop()를 사용하여 얻습니다.
    autopost: Optional[bool]
        자동으로 길드 정보를 등록된 토큰 값을 통하여 전송할지 설정합니다. 기본값은 False 입니다.
    autopost_interval: Optional[int]
        `autopost` 를 활성화하였을 때 작동하는 매개변수 입니다. 초단위로 주기를 설정합니다.
        기본값은 3600초(30분) 간격으로 설정됩니다. 만약 설정할 경우 무조건 900초(15분) 이상 설정해야합니다.
    """
    def __init__(self,
                 bot: discord.Client,
                 koreanbots_token: str = None,
                 topgg_token: str = None,
                 uniquebots_token: str = None,
                 session: aiohttp.ClientSession = None,
                 loop: asyncio.AbstractEventLoop = None,
                 autopost: bool = True,
                 autopost_interval: int = 3600):
        self.koreanbots_token = koreanbots_token
        self.topgg_token = topgg_token
        self.uniquebots_token = uniquebots_token
        self.client = bot
        self.http = HttpClient(koreanbots_token=koreanbots_token,
                               topgg_token=topgg_token,
                               uniquebots_token=uniquebots_token,
                               session=session,
                               loop=loop)

        self.autopost = autopost
        self.autopost_interval: int = autopost_interval
        self.loop = loop or self.client.loop

        if autopost:
            if self.autopost_interval < 900:
                raise ClientException("autopost_interval must be greater than or equal to 900 seconds(15 minutes)")

            self.autopost_task = self.loop.create_task(self._auto_post())

    async def _auto_post(self):
        """
        본 함수는 코루틴(비동기)함수 입니다.

        `discord.Client`의 .guilds 값에 있는 목록의 갯수를 읽어서 `stats()`를 통하여 각 API로 자동으로 보냅니다.
        만약에 아무 API 키가 없을 경우, 작동하지 않습니다. 최소 한 곳이상 등록해 주세요.
        """
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            if self.koreanbots_token == self.topgg_token == self.uniquebots_token is None:
                return
            log.info('Autoposting guild count.')
            try:
                await self.stats()
            except TooManyRequests:
                pass
            await asyncio.sleep(self.autopost_interval)

    def guild_count(self) -> int:
        """`discord.Client`의 .guilds 값에 있는 목록의 갯수를 읽어옵니다."""
        return len(self.client.guilds)

    async def bot(self, bot_id: int = None, web_type: List[WebsiteType] = None) -> WebsiteBot:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        봇 정보를 불러옵니다.

        Parameters
        ----------
        bot_id: Optional[int]
            봇 ID 값이 포함됩니다. 봇 ID 값이 포함되질 않을 경우, 자신의 봇 ID가 들어갑니다.
        web_type: Optional[list[WebsiteType]]
            값을 불러올 웹사이트를 선택하실 수 있습니다. 기본 값은 토큰 유/무에 따른 모든 웹클라이언트에 발송됩니다.
            배열 안에 있는 웹사이트 유형에 따라 일부 정보만 불러올 수 있습니다.
        Returns
        -------
        WebsiteBot:
            웹사이트로 부터 들어온 봇 정보가 포함되어 있습니다.
        """
        if bot_id is None:
            bot_id = self.client.user.id
        return await self.http.bot(bot_id=bot_id, web_type=web_type)

    async def stats(self, guild_count: int = None, web_type: List[WebsiteType] = None) -> WebsiteStats:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        봇 정보를 수신하거나 발신합니다.

        Notes
        -----
        top.gg 에서는 :meth:`guild_count` 외에도, `shard_count`, `shard_ids` 등의 다른 데이터도 수신할 수 있지만,
        기본 Client와 HttpClient에서는 지원하지 않습니다.

        Parameters
        ----------
        guild_count: Optional[int]
            서버 갯수가 포함되어 있습니다.
        web_type: Optional[list[WebsiteType]]
            값을 보낼 웹사이트를 선택하실 수 있습니다. 기본 값은 토큰 유/무에 따른 모든 웹클라이언트에 발송됩니다.
            배열 안에 있는 웹사이트 유형에 따라 일부 웹사이트에만 발송합니다.
        Returns
        -------
        WebsiteStats:
            웹사이트로 부터 들어온 봇 상태 정보가 포함되어 있습니다.
        """
        if guild_count is None:
            guild_count = self.guild_count()
        return await self.http.stats(bot_id=self.client.user.id, guild_count=guild_count, web_type=web_type)

    async def vote(self, user_id: int, web_type: List[WebsiteType] = None) -> WebsiteVote:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        `user_id`에 들어있는 사용자가 봇에 하트 혹은 투표를 누른 여부에 대하여 불러옵니다.

        Parameters
        ----------
        user_id: int
            유저 ID 값이 포함되어 있습니다.
        web_type: Optional[list[WebsiteType]]
            값을 불러올 웹사이트를 선택하실 수 있습니다. 기본 값은 토큰 유/무에 따른 모든 웹클라이언트에 발송됩니다.
            배열 안에 있는 웹사이트 유형에 따라 일부 정보만 불러올 수 있습니다.

        Returns
        -------
        WebsiteVote:
            웹사이트로 부터 들어온 사용자 투표 정보에 대한 정보가 포함되어 있습니다.
        """
        return await self.http.vote(bot_id=self.client.user.id, user_id=user_id, web_type=web_type)

    async def votes(self, web_type: List[WebsiteType] = None) -> WebsiteVotes:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        하트 혹은 투표를 누른 사용자 목록을 모두 불러옵니다.

        Notes
        -----
        koreanbots 에서는 사용자 하트 목록을 불러오지 못합니다. topgg 혹은 uniquebots 모델만 사용이 가능합니다.

        Parameters
        ----------
        web_type: Optional[list[WebsiteType]]
            값을 불러올 웹사이트를 선택하실 수 있습니다. 기본 값은 토큰 유/무에 따른 모든 웹클라이언트에 발송됩니다.
            배열 안에 있는 웹사이트 유형에 따라 일부 정보만 불러올 수 있습니다.

        Returns
        -------
        WebsiteVotes:
            웹사이트로 부터 들어온 봇 하트 정보가 포함되어 있습니다.
        """
        return await self.http.votes(bot_id=self.client.user.id, web_type=web_type)

    async def users(self, user_id: int, web_type: List[WebsiteType] = None) -> WebsiteUser:
        """
        본 함수는 코루틴(비동기)함수 입니다.

        사용자 정보를 불러옵니다.

        Parameters
        ----------
        user_id: int
            사용자 ID 값이 포함됩니다.
        web_type: Optional[list[WebsiteType]]
            값을 불러올 웹사이트를 선택하실 수 있습니다. 기본 값은 토큰 유/무에 따른 모든 웹클라이언트에 발송됩니다.
            배열 안에 있는 웹사이트 유형에 따라 일부 정보만 불러올 수 있습니다.

        Returns
        -------
        WebsiteUser
            웹사이트로 부터 들어온 사용자 정보가 포함되어 있습니다.
        """
        return await self.http.users(user_id=user_id, web_type=web_type)
