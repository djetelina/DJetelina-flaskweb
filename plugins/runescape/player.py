#!/usr/bin/env python
# coding=utf-8
import requests
from collections import namedtuple
from datetime import datetime

Activity = namedtuple('Activity', ['date', 'text', 'details'])
Quests = namedtuple('Quests', ['started', 'complete', 'not_started'])

skills = {
    0: 'Attack',
    1: 'Defence',
    2: 'Strength',
    3: 'Constitution',
    4: 'Ranged',
    5: 'Prayer',
    6: 'Magic',
    7: 'Cooking',
    8: 'Woodcutting',
    9: 'Fletching',
    10: 'Fishing',
    11: 'Firemaking',
    12: 'Crafting',
    13: 'Smithing',
    14: 'Mining',
    15: 'Herblore',
    16: 'Agility',
    17: 'Thieving',
    18: 'Slayer',
    19: 'Farming',
    20: 'Runecrafting',
    21: 'Hunter',
    22: 'Construction',
    23: 'Summoning',
    24: 'Dungeoneering',
    25: 'Divination',
    26: 'Invention'
}

def _parse_activity(item):
    return Activity(
        date=datetime.strptime(item['date'], '%d-%b-%Y %H:%M'),
        text=item['text'],
        details=item['details']
    )


class Player:
    def __init__(self, name='DJetelina'):
        self.name = name
        self._get_profile()

    def _get_profile(self):
        profile = requests.get(
            f'https://apps.runescape.com/runemetrics/profile/profile?user={self.name}&activities=20'
        ).json()
        self.activities = sorted(
            [_parse_activity(activity) for activity in profile['activities']],
            key=lambda k: k.date, reverse=True
        )
        self.combat_level = profile['combatlevel']
        self.logged_in = True if profile['loggedIn'] == 'true' else False
        self.skills = {skills[skill['id']]: {
            'level': skill['level'],
            'xp': skill['xp'],
            'rank': skill['rank']
        } for skill in profile['skillvalues']}
        self.rank = profile['rank']
        self.total_skill = profile['totalskill']
        self.total_xp = profile['totalxp']
        self.quests = Quests(
            started=profile['questsstarted'],
            complete=profile['questscomplete'],
            not_started=profile['questsnotstarted']
        )
