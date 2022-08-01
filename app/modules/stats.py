from flask import url_for
from riotwatcher import LolWatcher, ApiError
import pickle
import os
import time
from datetime import datetime


# config
api_key = 'your_api_key'
watcher = LolWatcher(api_key)

# download champion names from data dragon
champs_list = watcher.data_dragon.champions('12.14.1', False, 'en_US')['data']
new_champs_list = {}
for champion in champs_list:
    new_champs_list[champs_list[champion]['key']] = champion

# download item names from data dragon
items_list = watcher.data_dragon.items('12.14.1', 'en_US')['data']


class Player:
    def __init__(self, username, server):
        try: 
            # load data if exists
            self.username = username
            self.load()
        except:
            self.get_data(username,server)
    
    def get_data(self, username, server):
        self.username = username
        self.server = server
        self.error = 0
        try:
            self.data = watcher.summoner.by_name(server, username)
            watcherdata = watcher.league.by_summoner(server, self.data['id'])
            self.solo = {}
            self.flex = {}
            rank_data = ['tier','rank', 'leaguePoints', 'wins', 'losses']
            # assign player rank data
            if len(watcherdata) > 0:
                if watcherdata[0]['queueType'] == 'RANKED_SOLO_5x5':
                    for data in rank_data:
                        self.solo[data] = watcherdata[0][data]
                        self.flex[data] = 0
                    self.solo['tier'] = self.solo['tier'].lower()
                    self.solo['winrate'] = '{:.2f}'.format(self.solo['wins'] / (self.solo['wins'] + self.solo['losses']) * 100) + '%'
                    self.flex['winrate'] = 0
                else:
                    for data in rank_data:
                        self.flex[data] = watcherdata[0][data]
                        self.solo[data] = 0
                    self.flex['tier'] = self.flex['tier'].lower()
                    self.flex['winrate'] = '{:.2f}'.format(self.flex['wins'] / (self.flex['wins'] + self.flex['losses']) * 100) + '%'
                    self.solo['winrate'] = 0


                if len(watcherdata) > 1:
                    if watcherdata[1]['queueType'] == 'RANKED_FLEX_SR':
                        for data in rank_data:
                            self.flex[data] = watcherdata[1][data]
                        self.flex['tier'] = self.flex['tier'].lower()
                        self.flex['winrate'] = '{:.2f}'.format(self.flex['wins'] / (self.flex['wins'] + self.flex['losses']) * 100) + '%'
                    else:
                        for data in rank_data:
                            self.solo[data] = watcherdata[1][data]
                        self.solo['tier'] = self.solo['tier'].lower()
                        self.solo['winrate'] = '{:.2f}'.format(self.solo['wins'] / (self.solo['wins'] + self.solo['losses']) * 100) + '%'

            else:
                for data in rank_data:
                    self.solo[data] = 0
                    self.flex[data] = 0
                self.solo['data'] = 0
                self.flex['winrate'] = 0

            # assign matches list
            matches = watcher.match.matchlist_by_puuid(server, self.data['puuid'], 0, 5)
            self.matches_list = []
            for match in matches:
                match = Match(server, match)
                self.matches_list.append(match)

            # save instance
            self.save()

        except ApiError as err:
            if err.response.status_code == 429:
                self.error = 429
            elif err.response.status_code == 404:
                self.error = 404
            else:
                raise
        

    def save(self): 
        path = os.getcwd() + '/app/static/users/' + self.username + '.pickle'
        file = open(path, 'wb')
        file.write(pickle.dumps(self.__dict__))
        file.close()
    
    def load(self):
        path = os.getcwd() + '/app/static/users/' + self.username + '.pickle'
        file = open(path, 'rb')
        dataPickle = file.read()
        file.close()

        self.__dict__ = pickle.loads(dataPickle)


class Match():
    def __init__(self, server, id):
        # assign match details
        self.details = watcher.match.by_id(server, id)
        self.details['info']['teams'][0]['gold'] = 0
        self.details['info']['teams'][1]['gold'] = 0
        
        # match start timer
        self.game_start = datetime.fromtimestamp(int(self.details['info']['gameStartTimestamp']/1000))

        # assign participants stats
        self.participants = []

        # automation of participants stats assigning
        summoner_stats = ['summoner1Id', 'summoner2Id', 'win', 'kills', 'deaths', 'assists', 'totalDamageDealtToChampions',\
            'totalHealsOnTeammates', 'goldEarned', 'champLevel', 'totalMinionsKilled', 'visionScore']
        
        for index, row in enumerate(self.details['info']['participants']):
            if row['puuid'] != 'BOT':
                watcherdata = watcher.summoner.by_puuid(server, row['puuid'])
            else:
                watcherdata['name'] = 'BOT'
                watcherdata['summonerLevel'] = 30

            participants_row = {}
            
            if index <= 4:
                self.details['info']['teams'][0]['gold'] += row['goldEarned']
            else:
                self.details['info']['teams'][1]['gold'] += row['goldEarned']

            for stat in summoner_stats:
                participants_row[stat] = row[stat]
                
            participants_row['username'] = watcherdata['name']
            participants_row['level'] = watcherdata['summonerLevel']
            participants_row['champion'] = new_champs_list[str(row['championId'])]

            # automation of items assigning
            itemsid = ['item0', 'item1', 'item2', 'item3', 'item4', 'item5']
            for item in itemsid:
                if row[item] != 0:
                    participants_row[item] = row[item]

            self.participants.append(participants_row)

