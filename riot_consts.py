URL = {
    'summoner_by_name': 'https://{region}.api.riotgames.com/lol/summoner/v{version}/summoners/by-name/{name}',
    'matches_by_summoner_name': 'https://{proxy}.api.riotgames.com/lol/match/v{version}/matches/by-puuid/{puuid}/ids?type={type}&start=0&count=20',
    'current_game_by_summoner_name': 'https://{region}.api.riotgames.com/lol/spectator/v{version}/active-games/by-summoner/{id}',
    'game_timeline_by_match_id': 'https://{proxy}.api.riotgames.com/lol/match/v{version}/matches/{match_id}/timeline',
    'match_info_by_match_id': 'https://{proxy}.api.riotgames.com/lol/match/v5/matches/{match_id}',
    'all_league_entries_by_queue_tier_division': 'https://{region}.api.riotgames.com/lol/league/v{version}/entries/{queue}/{tier}/{division}',
    'league_entries_by_summoner_id': 'https://{region}.api.riotgames.com/lol/league/v{version}/entries/by-summoner/{encryptedSummonerId}',
    'champion_mastery_by_summoner_id_champion_id': 'https://{region}.api.riotgames.com/lol/champion-mastery/v{version}/champion-masteries/by-summoner/{encryptedSummonerId}/by-champion/{championId}',
    'champion_masteries_by_summoner_id': 'https://{region}.api.riotgames.com/lol/champion-mastery/v{version}/champion-masteries/by-summoner/{encryptedSummonerId}',
    'total_mastery_score_by_summoner_id': 'https://{region}.api.riotgames.com/lol/champion-mastery/v{version}/scores/by-summoner/{encryptedSummonerId}',

}

API_VERSIONS = {
    'summoner': '4',
    'match': '5',
    'spectator': '4',
    'league': '4',
    'champion-mastery': '4'
}

REGIONS = {
    'TR': 'tr1',
    'EUW': 'euw1'
}

PROXIES = {
    'TR': 'EUROPE',
    'EUW': 'EUROPE',
    'NA': 'AMERICAS'
}