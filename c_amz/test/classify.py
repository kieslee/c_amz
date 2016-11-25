
import sys
import json

'''
key_list = acache.get_keys()

for k in key_list:
    print acache.get_value(k)
    '''

print sys.argv
f = open(sys.argv[1])
con = f.read()

item_list = json.loads(con)

item_class = {}

for item in item_list:
    class_name = item['class_name']
    url = item['url']
    rank = item['rank']

    if item_class.has_key(class_name):
        continue

    item_class[class_name] = {'url': url, 'rank': rank}


output = []
for k in item_class:
    class_name = k
    item = item_class[k]
    item['class_name'] = class_name
    output.append(item)

fo = open(sys.argv[2], 'w')
fo.write(json.dumps(output))
fo.close()
