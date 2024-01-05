import csv
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import json


def gen_co(center_node_coordinate, radius, relevance):
    # Generate random distance and angle
    distance = random.uniform(0, radius)
    angle = random.uniform(0, 2 * math.pi)

    # Calculate x, y coordinates relative to the center node
    x = center_node_coordinate[0] + distance * math.cos(angle) * relevance/ 100
    y = center_node_coordinate[1] + distance * math.sin(angle) * relevance/ 100

    new_coordinate = (x, y)

    return new_coordinate

def loc_topic_co(topic, array):
  for i in array:
    if i['type'] == 'topic' and i['text'] == topic:
      return (i['longitude'],i['latitude'])
    else:
      continue

def loc_subtopic_co(subtopic, array):
  for i in array:
    if i['type'] == 'subtopic' and i['text'] == subtopic:
      return (i['longitude'],i['latitude'])
    else:
      continue

def gen_ran_relevant(minimun, maximum):
  return random.randint(minimun, maximum)

csvfile = open('data_to_test.csv',encoding='utf-8')   
raw_data = list(csv.reader(csvfile)) 

new_data_json = {'nodes':[]}


for i in raw_data[1:]:

  new_data = {'text':'',
            'type':'',
            'topic':'',
            'subtopic':'',
            'longitude':float,
            'latitude':float,
            'relevance':int,
            }

  new_data['text'] = i[0].strip()
  new_data['type'] = i[1].strip()
  new_data['topic'] = i[2].strip()
  new_data['subtopic'] = i[3].strip()
  
  if new_data['type'] == 'topic':
    new_data['longitude'] = 0
    new_data['latitude'] = 0
    new_data['relevance'] = 100

  elif new_data['type'] == 'subtopic':
    new_data['relevance'] = gen_ran_relevant(60, 90)
    parent_co = loc_topic_co(new_data['topic'],new_data_json['nodes'])
    if parent_co:
      (new_data['longitude'], new_data['latitude']) = gen_co(parent_co, 5, new_data['relevance'])
    

  elif new_data['type'] == 'sub-subtopic':
    new_data['relevance'] = gen_ran_relevant(1, 50)
    parent_co = loc_subtopic_co(new_data['subtopic'],new_data_json['nodes'])
    if parent_co:
      (new_data['longitude'], new_data['latitude']) = gen_co(parent_co, 1, new_data['relevance'])

  new_data_json['nodes'].append(new_data)


print (new_data_json)



with open('final_data.csv', 'w', newline='',encoding='utf-8') as file:
   writer = csv.writer(file)
   writer.writerow(['text','type','topic','subtopic','longitude','latitude','relevance'])
   for i in new_data_json['nodes']:
     writer.writerow([i['text'],i['type'],i['topic'],i['subtopic'],i['longitude'],i['latitude'],i['relevance']])

