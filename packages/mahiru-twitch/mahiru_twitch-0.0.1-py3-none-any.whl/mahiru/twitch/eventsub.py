import hashlib
import hmac
from dataclasses import dataclass
from typing import List

from aiohttp import web

from mahiru.core import Module


@dataclass
class User:
    id: str
    login: str
    name: str


class CallbackHandler:
    module: Module
    secret: bytes
    routes: List[web.RouteDef]

    def __init__(self, module, secret: str):
        self.module = module
        self.secret = secret.encode()
        self.routes = [
            web.post('/twitch/eventsub', lambda r: self.callback(r)),
        ]

    async def callback(self, request: web.Request):
        if await self.verify(request):
            message_type = request.headers['Twitch-Eventsub-Message-Type']
            data = await request.json()
            if message_type == 'webhook_callback_verification':
                print(f'verification with challenge {data["challenge"]}')
                return web.Response(body=data['challenge'])
            elif message_type == 'notification':
                if data['subscription']['type'] == 'channel.follow':
                    follower = User(
                        data['event']['user_id'],
                        data['event']['user_login'],
                        data['event']['user_name']
                    )
                    broadcaster = User(
                        data['event']['broadcaster_user_id'],
                        data['event']['broadcaster_user_login'],
                        data['event']['broadcaster_user_name']
                    )
                    await self.on_follow(follower, broadcaster)
                    return web.Response()
                else:
                    print(f'unknown notification "{data["subscription"]["type"]}"')
            else:
                print(f'Twitch EventSub unknown message type "{message_type}"')
                # TODO is there a better response to properly tell the server I cant handle this atm
                return web.Response(status=404)
        else:
            print('verifying twitch eventsub notification failed')

    async def on_follow(self, follower: User, broadcaster: User):
        await self.module.trigger_event('twitch_follow', {
            'follower_id': follower.id,
            'follower_name': follower.name,
            'follower_login': follower.login
        }, 'twitch', broadcaster.login)
        print(f'{follower.name} followed {broadcaster.name}')

    async def verify(self, request: web.Request) -> bool:
        signature = request.headers['Twitch-Eventsub-Message-Signature']
        message_id = request.headers['Twitch-Eventsub-Message-Id'].encode()
        timestamp = request.headers['Twitch-Eventsub-Message-Timestamp'].encode()
        body = await request.read()
        data = message_id + timestamp + body
        calculated = hmac.new(self.secret, data, hashlib.sha256).hexdigest()
        if 'sha256=' + calculated == signature:
            return True
        else:
            return False
