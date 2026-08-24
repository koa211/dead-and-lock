# final goal, open up a terminal, ask for a user input and search?
import pandas as pd
import urllib
import json
import requests
import re
from datetime import datetime

# plotting historgram
from matplotlib import pyplot as plt
import numpy as np

"""
json testing tool for parsing
"""


def get_match():
    unix_timestamp = int((datetime.now() - datetime(1970, 1, 2)).total_seconds())
    match_id = 98153446
    url = f"https://api.deadlock-api.com/v1/matches/{match_id}/metadata"

    response = requests.get(url)
    byte_j = json.dumps(response.json(), separators=(",", ":"), indent=4)

    with open("../../out.txt", "w") as file:
        file.write(byte_j)


def match_sum():
    obj_list = []
    time = None
    flag = False
    acc_id = 0
    player_dmg = 0

    with open("../../out.txt", "r") as file:
        # get first instance of duration_s
        for line in file:
            if time:
                break
            if "duration_s" in line:
                time = line[21:25]

        for line in file:
            if "account_id" in line:
                acc_id = ''.join(re.findall(r'\d', line))

            if "time_stamp_s" in line and line.strip()[15:19] == time:
                flag = True
            if flag == True and "player_damage" in line:
                player_dmg = ''.join(re.findall(r'\d', line))
                ply = Player(acc_id, player_dmg)
                obj_list.append(ply)
                flag = False

    print(obj_list)


class Player:
    def __init__(self, id, damage):
        self.id = id
        self.damage = damage

    def __repr__(self):
        return (self.id) + " " + (self.damage)


def get_avr_rank(rankcount):
    # for each of the match in out.txt get the average for that and then put that data in an array I guess 
    # open file out.txt and get 10 match_id
    ids = []
    with open("../../out.txt", "r") as file:
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

        byte_j = json.dumps(response.json(), separators=(",", ":"), indent=4)

        # get the 12 player rank
        with open("../../match.txt", "w") as file:
            file.write(byte_j)

        list_extracted_data = []
        with open("../../match.txt", "r") as file:
            for line in file:
                if "initial_display_rank" in line:
                    searched_phrase = re.search(r"\d+", line)
                    start_index, end_index = searched_phrase.start(), searched_phrase.end()
                    list_extracted_data.append(int(line[start_index:end_index]))
        calc_rank_and_display(list_extracted_data, rankcount)


def calc_rank_and_display(list_extracted_data, rankcount):
    unranked = 12
    total = 0
    for rank in list_extracted_data:
        if rank == 0:
            unranked -= 1
        total += rank

    final = int((total / unranked) / 10)
    rankcount[final] += 1


def draw_hist(rankcount):
    ranks = ['Obscurus', 'Initiate', 'Seeker', 'Acolyte', 'Sentinel', 'Mystic', 'Ritualist', 'Emissary', 'Oracle',
             'Phantom', 'Ascendant', 'Eternus']
    plt.bar(ranks, rankcount)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.tight_layout()
    plt.show()


def get_acc_name(account_id):
    url = requests.get(
        "https://api.deadlock-api.com/v1/players/steam-search",
        params={
            "search_query": account_id
        }
    )

    byte_j = json.dumps(url.json(), separators=(",", ":"), indent=4)
    data = json.loads(byte_j)
    print(data[0]['personaname'])


def main():
    rankcount = [0] * 12
    # get_match()
    # match_sum()
    get_acc_name(900172942)


if __name__ == '__main__':
    main()
