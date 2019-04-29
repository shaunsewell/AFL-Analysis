# data_scraper.py
# Created by Shaun Sewell on 24/4/19.
#
# Script for scraping afl stats from footywire.com.au
#

from bs4 import BeautifulSoup
import requests
import re

# Outline stats to gather
stats = ['Disposals', 'Kicks', 'Handballs', 'Marks', 
        'Tackles', 'Hitouts', 'Clearances', 'Clangers',
        'Frees For', 'Frees Against', 'Goals Kicked', 
        'Behinds Kicked', 'Rushed Behinds', 'Scoring Shots', 
        'Goal Assists', 'Inside 50s', 'Rebound 50s']
        
advanced_stats = ['Contested Possessions', 'Uncontested Possessions', 
                'Effective Disposals', 'Disposal Efficiency','Contested Marks', 
                'Marks Inside 50','One Percenters',
                'Bounces', 'Centre Clearances', 'Stoppage Clearances',
                'Score Involvements', 'Metres Gained', 'Turnovers',
                'Intercepts', 'Tackles Inside 50']

# Need to remove spaces from team names
converted_names = {'Gold Coast' : 'Gold_Coast', 'North Melbourne' : 'North_Melbourne', 
                    'Port Adelaide': 'Port_Adelaide', 'St Kilda': 'St_Kilda', 
                    'West Coast': 'West_Coast', 'Western Bulldogs': 'Western_Bulldogs'}

# Original Header for footywire.com.au 
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
# Removed the image references to reduce response data.

class DataScraper:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Referer":"http://www.google.com.au","Cache-Control":"max-age=0"}
        self.base_URL = "http://www.footywire.com/afl/footy/ft_match_statistics?mid="
        self.session_obj = requests.Session()
           
    #def convert_team_names(self, team_str):
              
    #def get_matches(self, start_match_id, end_match_id):

    def get_match(self, match_id):
        response = self.session_obj.get(self.base_URL + str(match_id), headers=self.headers)
        soup = BeautifulSoup(response.text, features="html.parser")
        # returns a page title of the form: 
        # Home Team defeated by Away Team at Venue Round Number Day, Date(dd,mm,yy)
        # Brisbane defeated by Collingwood at Gabba Round 5 Thursday, 18th April 2019

        # defeated by, defeats, drew with, defeat 

        seperators = ["defeated by", "defeats", "defeat", "drew"]
        split_title = None 
        for s in seperators:
            title = soup.find(string=re.compile(s))
            if title != None:
                #replace defeated by with defeated_by to making traversing the array simpler
                modified_title = title.replace('defeated by', 'defeated_by')

                #do the same for the multi word team names
                for key in converted_names:
                    modified_title = modified_title.replace(key, converted_names[key])

                split_title = modified_title.split(' ')
                # index 0 - 3 is 'AFL' 'Match' 'Statistics' ':' and can be ignored

                break
        home_team = split_title[4]
        away_team = split_title[6]
        print(home_team + " vs " + away_team)
    #def get_players(self, match_id):
        
    #def get_player(self, player_name):

class Match:
    def __init__(self, match_id, home_team, away_team, venue, round_number, date, attendance, home_team_stats, away_team_stats):
        self.match_id = match_id
        self.home_team = home_team
        self.away_team = away_team
        self.venue = venue
        self.round_number = round_number
        self.date = date
        self.attendance = attendance
        self.home_team_stats = home_team_stats
        self.away_team_stats = away_team_stats
        
class Player:
    def __init__(self, player_id, player_name, player_team, player_age, player_stats):
        self.player_id = player_id
        self.player_name = player_name
        self.player_team = player_team
        self.player_stats = player_stats
        
        
scraper = DataScraper()
for i in range(9307, 9720 + 1): 
    scraper.get_match(i)