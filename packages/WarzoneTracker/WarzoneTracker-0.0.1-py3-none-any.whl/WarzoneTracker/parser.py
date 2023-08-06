import statistics
import heapq
from datetime import datetime
from pytz import timezone
import pytz

class WarzoneTrackerParser:
    
    def __init__(self):
        pass

    def get_match_stats(self, player_username, match_info):
        base_username = player_username.split('#')[0]
        try:
            _ = match_info['data']['segments'][0]['stats']['kills']['value']
        except:
            return None
        try:
            if not [segment for segment in match_info['data']['segments'] if segment['attributes']['platformUserIdentifier'].lower() != base_username.lower()]:
                return None
        except:
            return None
        
        teams = {} # team_fifteen : {'bob':kd, 'mark':kd} and so on
        player_team = {}
        match_id     = match_info['data']['attributes']['id']
        player_count = match_info['data']['metadata']['playerCount']
        mode_name    = match_info['data']['metadata']['modeName']
        timestamp    = match_info['data']['metadata']['timestamp']
        team_count   = match_info['data']['metadata']['teamCount']
        match_kd     = match_info['data']['attributes']['avgKd']['avgKd']
        kd_histogram = match_info['data']['attributes']['kdHistogram']
        link = f'https://cod.tracker.gg/warzone/match/{match_id}?handle={base_username}'
        lifetime_wins = []
        lifetime_games = []
        
        highest_kds = []
        lowest_kds = []
        num_players_private = 0
        for player in match_info['data']['segments']:
            team = player['attributes']['team']
            if team in teams:
                teams[team].append(player)
            else:
                teams[team] = [player]

            curr_username = player['attributes']['platformUserIdentifier']
            if curr_username.lower() == base_username.lower():
                player_team = player['attributes']['team']
                placement = player['metadata']['placement']['value']
            
            if 'lifeTimeStats' in player['attributes']:
                lifetime_wins.append(player['attributes']['lifeTimeStats']['wins'])
                lifetime_games.append(player['attributes']['lifeTimeStats']['gamesPlayed'])
            else:
                num_players_private += 1
        teams_processed = {}
        highest_team_kd = 0
        highest_team_placement = 0
        my_team_kd = 0
        my_team = []
        for team_name, team in teams.items():
            avg = 0
            total = len(team)
            for person in team:
                try:
                    avg += person['attributes']['lifeTimeStats']['kdRatio']
                except Exception:
                    total -= 1
            avg = avg / total
            if avg > highest_team_kd:
                highest_team_kd = avg
            teams_processed[team_name] = avg
            if team_name == player_team:
                my_team_kd = avg
                for person in team:
                    try:
                        lifetime_stats = person['attributes']['lifeTimeStats']
                    except Exception:
                        lifetime_stats = None
                    my_team.append({
                        'name': person['attributes']['platformUserIdentifier'],
                        'lifetime_stats': lifetime_stats,
                        'url': person['metadata']['profileUrl'],
                        'kills': person['stats']['kills']['value']


                    })
        highest_lifetime_kd = []
        lowest_lifetime_kd = []
        heapq._heapify_max(kd_histogram)
        for _ in range(3):
            highest_lifetime_kd.append(heapq._heappop_max(kd_histogram))
        heapq.heapify(kd_histogram)
        for _ in range(3):
            lowest_lifetime_kd.append(heapq.heappop(kd_histogram))
        
        stats = {
            'date': match_info['data']['attributes']['id'],
            'match_kd': match_kd,
            'lifetime_wins':sum(lifetime_wins)/len(lifetime_wins),
            'lifetime_games':sum(lifetime_games)/len(lifetime_games),
            'highest_team_kd': highest_team_kd,
            'highest_lifetime_kd': highest_lifetime_kd,
            'lowest_lifetime_kd': lowest_lifetime_kd,
            'team': {
                'kd': my_team_kd,
                'placement': placement,
                'teammates': my_team
            }
        }
        return stats

    def get_player_kd(self, overview):
        kd = overview['data']['segments'][1]['stats']['kdRatio']['value']
        return kd

    def rank_last_k_lobbies(self, k, player_username):
        matches = self.get_k_matches(k, player_username)
        ids = []
        for match in matches:
            ids.append(match['attributes']['id'])
        kds = []
        for i in ids:
            kds.append((self.get_match_kd(i), i))
        return kds

    def get_match_kd(self, match_id):
        info = self.get_match_info(match_id)
        # entries: (0:lifetime_kd, 1:lifetime_wins, 2:lifetime_games, 3:lifetime_top5, 4:match_kd)
        lifetime_stats = []
        match_kds = []
        highest_kd = 0
        num_players_private = 0
        for player in info['data']['segments']:
            if 'lifeTimeStats' in player['attributes']:
                match_kd = player['stats']['kdRatio']['value']
                lifetime_kd = player['attributes']['lifeTimeStats']['kdRatio']
                wins = player['attributes']['lifeTimeStats']['wins']
                games = player['attributes']['lifeTimeStats']['gamesPlayed']
                top5 = player['attributes']['lifeTimeStats']['top5']
                lifetime_stats.append(
                    (lifetime_kd, wins, games, top5, match_kd))
                highest_kd = lifetime_kd if lifetime_kd > highest_kd else highest_kd
            else:
                num_players_private += 1
                match_kd = player['stats']['kdRatio']['value']
                match_kds.append(match_kd)
        mean_kd = statistics.mean([stat[0] for stat in lifetime_stats])
        median_kd = statistics.median([stat[0] for stat in lifetime_stats])
        match_mean = statistics.mean([stat for stat in match_kds])
        match_median = statistics.median([stat for stat in match_kds])
        return {'median_kd': median_kd, 'mean_kd': mean_kd, 'num_players_private': num_players_private, 'private_players_mean': match_mean, 'private_players_median': match_median}
    
    def convert_date(self, date, current_format, new_format, new_timezone):
        date = datetime.strptime(date, current_format)
        date = date.astimezone(timezone(new_timezone))
        return date.strftime(new_format)