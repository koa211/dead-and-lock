# final goal, open up a terminal, ask for a user input and search?
import pandas as pd
import urllib
import json
import requests
import re
"""
3 general statistic page for ranked 
what are we tracking?
- match distribution

3.1 get 10 most recent ranked matches of the day
3.2 for each individual match, get the rank of each player -> average that
"""
def get100():
    url = "https://api.deadlock-api.com/v1/matches/metadata"
    params = {
        'include_more_info': 'true', 
        'match_mode': 'ranked',
        'min_unix_timestamp': 1785826800,
        'limit': 10
        }
    
    response = requests.get(url, params=params)
    byte_j = json.dumps(response.json(), separators=(",",":"), indent=4)
    
    with open("out.txt", "w") as file:
        file.write(byte_j)
        
def get_avr_rank():
    # for each of the match in out.txt get the average for that and then put that data in an array I guess 
    # open file out.txt and get 10 match_id
    ids = []
    with open("out.txt", "r") as file:
        for line in file:
            if "match_id" in line:
                ids.append(int(line.strip()[11:19]))
    
    for i in range(len(ids)):
        cur_match_id = ids[i]
        
        url = f"https://api.deadlock-api.com/v1/matches/{cur_match_id}/metadata"
        # params = {
        #     'match_id': cur_match_id
        # }
        
        response = requests.get(url)
        
        byte_j = json.dumps(response.json(), separators=(",",":"), indent=4)
        
        # get the 12 player rank
        with open("match.txt", "w") as file:
                file.write(byte_j)
                
        list_extracted_data = []
        with open("match.txt", "r") as file:
                for line in file:
                    if "initial_display_rank" in line:
                        searched_phrase = re.search(r"\d+", line)
                        start_index, end_index = searched_phrase.start(), searched_phrase.end()
                        list_extracted_data.append(int(line[start_index:end_index]))
        calc_rank(list_extracted_data)           

def calc_rank(list_extracted_data):
    dict = {
        1 : 'Initiate',
        2 : 'Seeker',
        3 : 'Acolyte',
        4 : 'Sentinel',
        5 : 'Mystic',
        6 : 'Ritualist',
        7 : 'Emissary',
        8 : 'Oracle',
        9 : 'Phantom',
        10 : 'Ascendant',
        11 : 'Eternus'
    }
    unranked = 12
    total = 0
    for rank in list_extracted_data:
        if rank == 0:
            unranked -= 1
        total += rank
        
    final = int((total / unranked) / 10)
    print(dict.get(final))
               

def main():    
    get100()
    get_avr_rank()
    
if __name__ == '__main__':
    main()
