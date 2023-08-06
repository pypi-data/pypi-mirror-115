from typing import List, Tuple

from aiohttp.web import RouteDef
from twitch_helix import HelixClient
from twitch_helix.models import *
from twitch_ws_irc.client import TwitchWSIRCClient
from twitch_ws_irc.events import EventHandler as TwitchEventHandler, PrivMsgEvent

from mahiru.core import Module, Event as MahiruEvent, EventPool
from .eventsub import CallbackHandler


class TwitchModule(Module, TwitchEventHandler):
    channel: str
    client: TwitchWSIRCClient
    eventsub_handler: CallbackHandler
    eventsub_callback: str
    eventsub_secret: str
    helix: HelixClient

    def __init__(self, event_pool: EventPool, token, username, channel, client_id, client_secret, redirect_uri, scope,
                 helix_filename, callback_url, eventsub_secret):
        super().__init__(event_pool)
        self.channel = channel
        self.client = TwitchWSIRCClient(token, username, channel)
        self.eventsub_handler = CallbackHandler(self, eventsub_secret)
        self.eventsub_callback = callback_url
        self.eventsub_secret = eventsub_secret
        self.helix = HelixClient(client_id, client_secret, redirect_uri, scope, helix_filename)

    async def start(self):
        await self.client.start(self)
        subs = self.helix.eventsub_list()
        for sub in subs:
            self.helix.eventsub_delete(sub['id'])
        user = self.helix.get_user(login_name=self.channel)
        self.helix.eventsub_subscribe(
            'channel.follow', '1',
            BroadcasterCondition(user['id']),
            Transport(
                'webhook',
                f'{self.eventsub_callback}/twitch/eventsub',
                self.eventsub_secret
            )
        )

    def get_routes(self) -> Tuple[None, List[RouteDef]]:
        return None, self.eventsub_handler.routes

    async def consume(self, mahiru_event: MahiruEvent):
        if mahiru_event.name == 'reply' and mahiru_event.source.name == 'twitch':
            await self.client.send_message(mahiru_event.data['message'])
        if mahiru_event.name == 'twitch_follow':
            await self.client.send_message(f'Thank you very much for following')

    async def on_privmsg(self, event: PrivMsgEvent):
        print(f"{event.user}: {event.message}")
        await self.trigger_event('raw_message',
                                 {'message': event.message, 'user': event.user},
                                 'twitch', event.channel)
