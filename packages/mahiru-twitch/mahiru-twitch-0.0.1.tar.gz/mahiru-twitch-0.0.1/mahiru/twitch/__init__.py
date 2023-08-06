from .module import TwitchModule


def initialize(event_pool, token, username, channel, client_id, client_secret, redirect_uri, scope, helix_filename,
               callback_url, eventsub_secret):
    return TwitchModule(event_pool, token, username, channel, client_id, client_secret, redirect_uri, scope,
                        helix_filename, callback_url, eventsub_secret)
