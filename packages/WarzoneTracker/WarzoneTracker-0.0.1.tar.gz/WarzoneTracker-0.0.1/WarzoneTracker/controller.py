from api import WarzoneTrackerApi
from parser import WarzoneTrackerParser

if __name__ =='__main__':
    api = WarzoneTrackerApi()
    parser = WarzoneTrackerParser()
    username = 'zombieslaya3#1152'
    url_username = api._convert_username(username)
    overview = api.get_overview(username)
    kd = parser.get_player_kd(overview)
    print(kd)
