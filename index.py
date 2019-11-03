import requests
import xml.etree.ElementTree as ET
import os
import create_index
import add_doc

players_url = 'https://gd2.mlb.com/components/game/mlb/year_2014/month_06/day_18/gid_2014_06_18_colmlb_lanmlb_1' \
              '/players.xml'
players_resp = requests.get(players_url)
players_xml_file = 'my_players.xml'

with open(players_xml_file, 'wb') as f:
    f.write(players_resp.content)

stat_info = os.stat(players_xml_file)
print(players_xml_file + ': ' + str(round(stat_info.st_size / 1024)) + ' KB/n')

tree = ET.parse(players_xml_file)
game = tree.getroot()
teams = game.findall('./team')
players_dict = {}

for team in teams:
    players = team.findall('player')

    for player in players:
        players_dict[player.attrib.get('id')] = player.attrib.get('first') + ' ' + player.attrib.get('last')

innings_url = 'https://gd2.mlb.com/components/game/mlb/year_2014/month_06/day_18/gid_2014_06_18_colmlb_lanmlb_1' \
              '/inning/inning_all.xml'
innings_resp = requests.get(innings_url)
innings_xml_file = 'my_innings.xml'

with open(innings_xml_file, 'wb') as f:
    f.write(innings_resp.content)

innings_info = os.stat(innings_xml_file)
print(innings_xml_file + ': ' + str(round(stat_info.st_size / 1024)) + ' KB/n')

tree = ET.parse(innings_xml_file)
root = tree.getroot()

frames = ['top', 'bottom']
pitch_dictionary = {'FA': 'fastball', 'FF': '4-seam fb', 'FT': '2-seam fb', 'FC': 'fb-cutter', '': 'unknown',
                    None: 'none', 'FS': 'fb-splitter', 'SL': 'slider', 'CH': 'changeup', 'CU': 'curveball',
                    'KC': 'knuckle-curve', 'KN': 'knuckleball', 'EP': 'eephus', 'UN': 'unidentified',
                    'PO': 'pitchout', 'SI': 'sinker', 'SF': 'split-finger'}
total_pitch_count = 0
innings = root.findall('./inning')

pitchers_dict = {}
pitchers_count = {}

for inning in innings:
    for i in range(len(frames)):
        fr = inning.find(frames[i])
        if fr is not None:
            for ab in fr.iter('atbat'):

                batter_name = players_dict[ab.get('batter')]
                pitcher_name = players_dict[ab.get('pitcher')]

                if pitcher_name in pitch_dictionary:
                    pitch_dictionary[pitcher_name] += 1
                else:
                    pitch_dictionary[pitcher_name] = 1

                create_index.create(pitcher_name)

                ab_pitch_count = 0

                pitches = ab.findall('pitch')

                for pitch in pitches:

                    if pitcher_name in pitchers_count:
                        pitchers_count[pitcher_name] += 1
                    else:
                        pitchers_count[pitcher_name] = 1

                    ab_pitch_count += 1
                    pitch_type = pitch_dictionary[pitch.get('pitch_type')]
                    pitch_des = pitch.get('des')
                    start_speed = float(pitch.get('start_speed'))
                    end_speed = float(pitch.get('end_speed'))
                    nasty = int(pitch.get('nasty'))
                    type_confidence = float(pitch.get('type_confidence'))

                    pitch_body = {'Batter': batter_name, 'Decision': pitch_des, 'Pitch Type': pitch_type,
                                  'Start Speed': start_speed, 'End Speed': end_speed, 'Nasty': nasty,
                                  'Type Confidence': type_confidence}

                    add_doc.add_document(pitcher_name, pitchers_count[pitcher_name], 'pitch', pitch_body)
