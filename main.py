# final goal, open up a terminal, ask for a user input and search?
import pandas as pd
import urllib
import json
import requests
"""
3 general statistic page for ranked
3.1 get 100 most recent ranked matches of the day
"""
def get100():
    url = "https://api.deadlock-api.com/v1/matches/metadata"
    params = {
        'include_more_info': 'true', 
        'match_mode': 'ranked',
        'min_unix_timestamp': 1785826800,
        'limit': 5
        }
    
    response = requests.get(url, params=params)
    
    print(response)
    

def main():    
    get100()

if __name__ == '__main__':
    main()
