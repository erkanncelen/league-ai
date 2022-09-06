import pandas as pd
import requests

import riot_api_key as riot_api_key
import riot_consts as consts

ddragon_version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]
ddragon_items = requests.get(
    ('http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json').format(
        version=ddragon_version)).json()
ddragon_champions = requests.get(
    ('http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/championFull.json').format(
        version=ddragon_version)).json()

champions = pd.DataFrame.from_dict(ddragon_champions['data'], orient='index')
items = pd.DataFrame.from_dict(ddragon_items['data'], orient='index')


class riot_api(object):

    # CORE
    def __init__(self, api_key=riot_api_key.KEY, region='TR'):
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = requests.get(url=api_url, params=args)
        print(response.url)
        return response.json()

    # SUMMONER ENDPOINT
    def get_summoner_by_name(self, name):
        api_url = consts.URL['summoner_by_name'].format(
            region=consts.REGIONS[self.region],
            version=consts.API_VERSIONS['summoner'],
            name=name
        )
        return self._request(api_url)

    # SPECTATOR ENDPOINT
    def get_current_game_by_summoner_name(self, name):
        summoner = self.get_summoner_by_name(name)
        api_url = consts.URL['current_game_by_summoner_name'].format(
            region=consts.REGIONS[self.region],
            version=consts.API_VERSIONS['spectator'],
            id=summoner['id']
        )

        return self._request(api_url)

    # MATCH ENDPOINT
    def get_matches_by_summoner_name(self, name, type='ranked'):
        summoner = self.get_summoner_by_name(name)

        api_url = consts.URL['matches_by_summoner_name'].format(
            proxy=consts.PROXIES[self.region],
            version=consts.API_VERSIONS['match'],
            puuid=summoner['puuid'],
            type=type
        )
        return self._request(api_url)

    def get_game_timeline_by_match_id(self, match_id):
        api_url = consts.URL['game_timeline_by_match_id'].format(
            proxy=consts.PROXIES[self.region],
            version=consts.API_VERSIONS['match'],
            match_id=match_id
        )
        return self._request(api_url)

    def get_match_info_by_match_id(self, match_id):
        api_url = consts.URL['match_info_by_match_id'].format(
            proxy=consts.PROXIES[self.region],
            version=consts.API_VERSIONS['match'],
            match_id=match_id
        )
        return self._request(api_url)

    

    # LEAGUE ENDPOINT
    def get_all_league_entries_by_queue_tier_division(self, queue='RANKED_SOLO_5x5', tier='PLATINUM', division='IV'):
        api_url = consts.URL['all_league_entries_by_queue_tier_division'].format(
            region=consts.REGIONS[self.region],
            version=consts.API_VERSIONS['league'],
            queue=queue,
            tier=tier,
            division=division)
        return self._request(api_url)

    def get_league_entries_by_summoner_id(self, summoner_id):
        api_url = consts.URL['league_entries_by_summoner_id'].format(
            region=consts.REGIONS[self.region],
            version=consts.API_VERSIONS['league'],
            encryptedSummonerId=summoner_id)
        return self._request(api_url)

    # CHAMPION MASTERY ENDPOINT
    def get_champion_mastery_by_summoner_id_champion_id(self, summoner_id, champion_id):
        api_url = consts.URL['champion_mastery_by_summoner_id_champion_id'].format(
            region=consts.REGIONS[self.region],
            version=consts.API_VERSIONS['champion-mastery'],
            encryptedSummonerId=summoner_id,
            championId=champion_id)
        return self._request(api_url)

    def get_champion_masteries_by_summoner_id(self, summoner_id):
        api_url = consts.URL['champion_masteries_by_summoner_id'].format(
            region=consts.REGIONS[self.region],
            version=consts.API_VERSIONS['champion-mastery'],
            encryptedSummonerId=summoner_id)
        return self._request(api_url)

    def get_total_mastery_score_by_summoner_id(self, summoner_id):
        api_url = consts.URL['total_mastery_score_by_summoner_id'].format(
            region=consts.REGIONS[self.region],
            version=consts.API_VERSIONS['champion-mastery'],
            encryptedSummonerId=summoner_id)
        return self._request(api_url)

