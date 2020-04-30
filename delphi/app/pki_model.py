import json

f = open('room_pc.json')
data = json.load(f)
count_data = {}
for room in data['classes']:
    count_data.update({room.get("Room#"): room.get("Count")})

vertices = ['t1', 't2', 's1', 's2', 's3', 'h1', 'h2', 'h5']
l2vertices = ['t3', 't4', 'h3', 'h4']
l3vertices = ['h6']
edges = {"sa": [("s1", 1000), ("s2", 1000), ('s3', 1000)], "s1": [("h1", count_data.get('s1'))],
         "s2": [("h1", count_data.get('s2'))], "s3": [("h1", count_data.get('s3'))], "h1": [("h2", 80)],
         "h2": [("h5", 75), ("t1", 25)], "t1": [("ta", 1000)], "t2": [("ta", 1000)], "h5": [("t2", 80)]}
l2edges = {"s1": [("h1", count_data.get('s1') / 2), ("h3", count_data.get('s1') / 2)], "h3": [("h4", 1)],
           "h4": [("t3", 1), ("t4", 1)], "t3": [("ta", 1000)],
           "t4": [("ta", 1)]}
l3edges = {"s3": [("h1", count_data.get('s3') / 2), ("h6", count_data.get('s3') / 2)], "h6": [("h4", 1)]}
