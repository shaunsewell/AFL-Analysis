# data_scraper.py
# Created by Shaun Sewell on 24/4/19.
#
# Script for scraping afl stats from footywire.com.au
#

from bs4 import BeautifulSoup
import requests
import re
from progress.bar import Bar
import csv

# Outline stats to gather
stats = ['Disposals', 'Kicks', 'Handballs', 'Marks', 
        'Tackles', 'Hitouts', 'Clearances', 'Clangers',
        'Frees For', 'Frees Against', 'Goals Kicked', 
        'Behinds Kicked', 'Rushed Behinds', 'Scoring Shots', 
        'Goal Assists', 'Inside 50s', 'Rebound 50s']
        
advanced_stats = ['Contested Possessions', 'Uncontested Possessions', 
                'Effective Disposals', 'Disposal Efficiency %','Contested Marks', 
                'Marks Inside 50','One Percenters',
                'Bounces', 'Centre Clearances', 'Stoppage Clearances',
                'Score Involvements', 'Metres Gained', 'Turnovers',
                'Intercepts', 'Tackles Inside 50']

# Need to remove spaces from team names
converted_names = {'Gold Coast' : 'Gold_Coast', 'North Melbourne' : 'North_Melbourne', 
                    'Port Adelaide': 'Port_Adelaide', 'St Kilda': 'St_Kilda', 
                    'West Coast': 'West_Coast', 'Western Bulldogs': 'Western_Bulldogs'}
#-----------------------------------------------------------------------------------------------------------------------
# Convenience functions
def export_matches(list_of_matches, file_name):

        stat_list = []

        with Bar('Processing stats for export', max=len(match_list), suffix='%(percent)d%% - %(eta)ds remaining') as stats_bar:
            for match in list_of_matches:
                home_stat_line = [match.round_number, match.venue, match.day, match.date, match.attendance, match.home_team]
                for keys in match.home_team_stats:
                    home_stat_line.append(match.home_team_stats[keys])
                stat_list.append(home_stat_line)

                away_stat_line = [match.round_number, match.venue, match.day, match.date, match.attendance, match.away_team]
                for keys in match.away_team_stats:
                    away_stat_line.append(match.away_team_stats[keys])
                stat_list.append(away_stat_line)
                stats_bar.next()
            stats_bar.finish()


        with Bar('Exporting', max=len(stat_list), suffix='%(percent)d%% - %(eta)ds remaining') as export_bar:
            with open(file_name, mode='w') as stats_file:
                stats_writer = csv.writer(stats_file, delimiter=',')
                for row in stat_list:
                    stats_writer.writerow(row)
                    export_bar.next()
            export_bar.finish()
#-----------------------------------------------------------------------------------------------------------------------

class DataScraper:
    def __init__(self):
        # Original Header for footywire.com.au 
        # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
        # Removed the image references to reduce response data.
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Referer":"http://www.google.com.au","Cache-Control":"max-age=0"}
        self.base_URL = "http://www.footywire.com/afl/footy/ft_match_statistics?mid="
        self.session_obj = requests.Session()
           
    def fix_title_string(self, soup):
        # Home Team defeated by Away Team at Venue Round Number Day, Date(dd,mm,yy)
        # St Kilda defeated by Melbourne at Marvel Stadium Round 1 Saturday, 25th March 2017
        # After spliting: 
        # ['AFL', 'Match', 'Statistics', ':', 'St_Kilda', 'defeated_by', 'Melbourne', 
        # 'at', 'Marvel', 'Stadium', 'Round', '1', 'Saturday,', '25th', 'March', '2017']

        seperators = ["defeated by", "defeats", "defeat", "drew"]
        for s in seperators:
            title = soup.find(string=re.compile(s))
            if title != None:
                #replace defeated by with defeated_by to making traversing the array simpler
                modified_title = title.replace('defeated by', 'defeated_by')

                #do the same for the multi word team names
                for key in converted_names:
                    modified_title = modified_title.replace(key, converted_names[key])

                split_title = modified_title.split(' ')
                return split_title
        
    def get_matches(self, start_match_id, end_match_id):
        Matches = []
        with Bar('Getting Matches', max=(end_match_id + 1) - start_match_id, suffix='%(percent)d%% - %(eta)ds remaining') as bar:
            for id in range(start_match_id, end_match_id + 1): 
                match = self.get_match(id)
                Matches.append(match)
                bar.next()
            bar.finish()
        return Matches
    
    def get_match(self, match_id):
        response = self.session_obj.get(self.base_URL + str(match_id), headers=self.headers)
        soup = BeautifulSoup(response.text, features="html.parser")
        # returns a page title of the form: 
        

        split_title = self.fix_title_string(soup) 
        # index 0 - 3 is 'AFL' 'Match' 'Statistics' ':' and can be ignored
        # Set home and away teams
        home_team = split_title[4]
        away_team = split_title[6]

        # Set the venue and round number
        venue = ""
        round_number = ""
        if split_title[9] == 'Round':
            venue = split_title[8]
            round_number = split_title[10]
        elif split_title[10] == 'Round': 
            venue = split_title[8] + " " + split_title[9]
            round_number = split_title[11]
        elif split_title[11] == 'Round':
            venue = split_title[8] + " " + split_title[9] + " " + split_title[10]
            round_number = split_title[12]
        else: # Must be a final
            if split_title[10] == 'Final':
                venue = split_title[8]
                round_number = split_title[9] + " " + split_title[10]
            elif split_title[11] == 'Final': 
                venue = split_title[8] + " " + split_title[9]
                round_number = split_title[10] + " " + split_title[11]


        # Set the day and date of the match
        day = split_title[-4].replace(',','')
        date = split_title[-3] + ' ' + split_title[-2] + ' ' + split_title[-1]

        # Set the attendance
        attendance_string = soup.find(text=re.compile('Attendance:')).split(' ')
        attendance = attendance_string[-1]

        # Get the stats
        home_team_stats, away_team_stats = self.get_stats(soup)
        home_team_stats, away_team_stats = self.get_advanced_stats(match_id, home_team_stats, away_team_stats)
        home_team_stats, away_team_stats = self.get_match_winner(soup, home_team_stats, away_team_stats)
        return Match(match_id, home_team, away_team, venue, round_number, day, date, attendance, home_team_stats, away_team_stats)
    
    def get_stats(self, soup):
        home_stats = {}
        away_stats = {}

        for stat in stats:
            stat_row = soup.find_all('td', text=stat)[0].find_parent('tr')
            stat_elements = stat_row.find_all('td')

            if stat_elements != None:
                if stat_elements[0].text == '-':
                    home_stats[stat] = None
                else:
                    home_stats[stat] = stat_elements[0].text
                
                if stat_elements[2].text == '-':
                    away_stats[stat] = None
                else:
                    away_stats[stat] = stat_elements[2].text
            

        return home_stats, away_stats

    def get_advanced_stats(self, match_id, home_stats, away_stats):
        response = self.session_obj.get(self.base_URL + str(match_id) + "&advv=Y", headers=self.headers)
        advanced_soup = BeautifulSoup(response.text, features="html.parser")

        for stat in advanced_stats:
            advanced_stat_row = advanced_soup.find_all('td', text=stat)[0].find_parent('tr')
            advanced_stat_elements = advanced_stat_row.find_all('td')
            
            if advanced_stat_elements != None:
                #Remove any annoying % signs
                temp_home = advanced_stat_elements[0].text.replace('%','')
                temp_away = advanced_stat_elements[2].text.replace('%','')

                if temp_home == '-':
                    home_stats[stat] = None
                else:
                    home_stats[stat] = temp_home
                
                if temp_away == '-':
                    away_stats[stat] = None
                else:
                    away_stats[stat] = temp_away
        
        return home_stats, away_stats

    def get_match_winner(self, soup, home_stats, away_stats):
        end_result = soup.find_all('td', text='End of Game')[0].find_parent('tr')
        end_result_element = end_result.find_all('td')
        if 'Won' in end_result_element[0].text:
            home_stats['Winner'] = 1
            away_stats['Winner'] = 0
        elif 'Won' in end_result_element[2].text:
            home_stats['Winner'] = 0
            away_stats['Winner'] = 1
        else:
            home_stats['Winner'] = 0
            away_stats['Winner'] = 0
        
        return home_stats, away_stats


    #def get_players(self, match_id):
        
    #def get_player(self, player_name):

class Match:
    def __init__(self, match_id, home_team, away_team, venue, round_number, day, date, attendance, home_team_stats, away_team_stats):
        self.match_id = match_id
        self.home_team = home_team
        self.away_team = away_team
        self.venue = venue
        self.round_number = round_number
        self.day = day
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
        
#-----------------------------------------------------------------------------------------------------------------------
# Testing implementation of functions  

scraper = DataScraper()
match_list = scraper.get_matches(9514, 9720) #9720
export_matches(match_list, "MatchStats2018.csv")

# Layout of columns in season match list
# column_headers = ['Round', 'Venue', 'Day', 'Date', 'Attendance', 'Team','Disposals', 'Kicks', 
#                 'Handballs', 'Marks', 'Tackles', 'Hitouts', 'Clearances', 'Clangers',
#                 'Frees For', 'Frees Against', 'Goals Kicked', 'Behinds Kicked',
#                 'Rushed Behinds', 'Scoring Shots', 'Goal Assists', 'Inside 50s',
#                 'Rebound 50s', 'Contested Possesions', 'Uncontested Possesions',
#                 'Effective Disposals', 'Disposal Efficiency %', 'Contested Marks',
#                 'Marks Inside 50', 'One Percenters', 'Bounces', 'Centre Clearances',
#                 'Stoppage Clearances', 'Score Involvments', 'Metres Gained', 'Turnovers',
#                 'Intercepts', 'Tackles Inside 50', 'Winner']

