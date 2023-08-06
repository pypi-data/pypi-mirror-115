import urllib.parse
import requests

class WarzoneTrackerApi:

    headers = {
        'authority': 'api.tracker.gg',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__cfduid=da33e6ee048785828f223ee2a65b3e78d1617577303; X-Mapping-Server=s8; __cflb=02DiuFQAkRrzD1P1mdm8JatZXtAyjoPD2o7G16pDofmnL',
    }

    def __init__(self):
        self.overview     = 'https://api.tracker.gg/api/v2/warzone/standard/profile/battlenet/{}/' # .format(username_of_battlenet)
        self.matches      = 'https://api.tracker.gg/api/v2/warzone/standard/matches/battlenet/{}?type=wz' # .format(username_of_battlenet)
        self.matches_next = 'https://api.tracker.gg/api/v2/warzone/standard/matches/battlenet/{}?type=wz&next={}' # .format(username_of_battlenet, next_id)
        self.match_info   = 'https://api.tracker.gg/api/v2/warzone/standard/matches/{}' # .format(username_of_battlenet)

    def get_overview(self, player_username):
        endpoint = self.overview.format(
            self._convert_username(player_username))
        r = requests.get(endpoint, headers=WarzoneTrackerApi.headers)
        return r.json()

    def get_k_matches(self, k, player_username):
        endpoint = self.matches.format(self._convert_username(player_username))
        r = requests.get(endpoint, headers=WarzoneTrackerApi.headers)
        info = r.json()
        try:
            matches = info['data']['matches']
            n = len(matches)
            next_match = info['data']['metadata']['next']
        except Exception as e:
            if 'errors' in info:
                return info['errors']
            return e
        while k > n:
            endpoint = self.matches_next.format(
                self._convert_username(player_username), next_match)
            r = requests.get(endpoint, headers=WarzoneTrackerApi.headers)
            info = r.json()
            try:
                matches += info['data']['matches']
                n += (len(matches) - n)
                next_match = info['data']['metadata']['next']
            except Exception as e:
                if 'errors' in info:
                    print(info['errors'])
                print(e)
                k = n
                break
        return matches[:k]
    
    def get_matches(self, player_username):
        endpoint = self.matches.format(self._convert_username(player_username))
        r = requests.get(endpoint, headers=WarzoneTrackerApi.headers)
        matches = r.json()
        if 'errors' in matches:
            return matches['errors']
        return matches

    def get_match_info(self, match_id):
        endpoint = self.match_info.format(match_id)
        r = requests.get(endpoint, headers=WarzoneTrackerApi.headers)
        return r.json()
    
    def _convert_username(self, username):
        return urllib.parse.quote(username)
