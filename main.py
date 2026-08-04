# final goal, open up a terminal, ask for a user input and search?
import pandas as pd
import http.client
import requests
import json

import heapq
"""
1 ask for the user to enter a champ name, run the API that returns their most bought items 

2 top 3 most banned heroes
"""
def hero_desc():
    name = input("Enter a champ name ")
    response = requests.get(f"https://api.deadlock-api.com/v1/assets/heroes/by-name/{name}")   
    byte_j = json.loads(response.content.decode('utf-8'))
    description = byte_j["description"]
    
    print(description)
    
def map_setup(id_to_hero):
    response = requests.get("https://api.deadlock-api.com/v1/assets/heroes")
    byte_j = json.loads(response.content.decode('utf-8'))
        
    # put this in a HM
    for i in byte_j:
        id_to_hero[i["id"]] = i["name"]
        
def hero_bans(id_to_hero):
    # call hero bans API, make a list of the top 3 highest
    response = requests.get("https://api.deadlock-api.com/v1/analytics/hero-ban-stats")
    byte_j = json.loads(response.content.decode('utf-8'))
    sort_list = sorted(byte_j, key=lambda d: d['bans'], reverse=True)
     
    # print name of char of top 3 highest bans
    top_ban = []
    for i in range(3):
        # extract id
        id = sort_list[i]["hero_id"]
        hero = id_to_hero[id]
        top_ban.append(hero)
        
    print(top_ban)

def main():    
    # hero_desc()
    id_to_hero = {}
    map_setup(id_to_hero)
    hero_bans(id_to_hero)

if __name__ == '__main__':
    main()
