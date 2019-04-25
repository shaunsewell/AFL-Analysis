# data_scrapper.py
# Created by Shaun Sewell on 24/4/19.
#
# Script for scrapping afl stats from footywire.com.au
#

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

class DataScrapper:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Referer":"http://www.google.com.au","Cache-Control":"max-age=0"}
        self.baseURL = "http://www.footywire.com/afl/footy/ft_match_statistics?mid="
        
    def convert_team_names(self, team_str):
                
    def get_matches(self, start_match_id, end_match_id):
    
    def get_match(self, match_id):

    def get_players(self, match_id):
        
    def get_player(self, player_name):

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
    def def __init__(self, player_id, player_name, player_team, player_age, player_stats):
        self.player_id = player_id
        self.player_name = player_name
        self.player_team = player_team
        self.player_stats = player_stats
        