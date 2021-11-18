import re
import requests

GAME_DATA_ENDPOINT = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
MINION_INFO_ENDPOINT = 'https://raw.communitydragon.org/latest/game/data/characters/{minion}/{minion}.bin.json'
DEFAULT_RADIUS = 65.
DEFAULT_WINDUP = 0.3
MINION_NAMES = ["sru_chaosminionmelee", "sru_chaosminionranged", "sru_chaosminionsiege", "sru_chaosminionsuper", "sru_orderminionmelee", "sru_orderminionranged", "sru_orderminionsiege", "sru_orderminionsuper"]


class MinionStats():
    def __init__(self):
        game_data = requests.get(GAME_DATA_ENDPOINT, verify=False).json()
        self.minion_data = {}
        for minion in MINION_NAMES:
            minion_response = requests.get(MINION_INFO_ENDPOINT.format(minion=minion)).json()
            # lower case everything for consistency
            self.minion_data[minion] = {k.lower(): v for k, v in minion_response.items()}

    def get_radius(self, target):
        root_key = 'characters/{}/characterrecords/root'.format(target.lower())
        radius = DEFAULT_RADIUS
        if target.lower() in self.minion_data.keys():
            radius = self.minion_data[target.lower()][root_key].get('overrideGameplayCollisionRadius', DEFAULT_RADIUS)
        return radius

    def names(self):
        return self.minion_data.keys()
