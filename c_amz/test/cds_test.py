import sys
import json
import uuid
import requests

def get_10_items():
    with open(sys.argv[1], 'r') as f:
        content = f.read()

    content_dict = json.loads(content)
    i = 0
    mini_content_dict = []
    for item in content_dict:
        if i >= 10:
            break
        mini_content_dict.append(item)
        i += 1

    f_w = open(sys.argv[2], 'w')
    f_w.write(json.dumps(mini_content_dict))
    f_w.close()


def post_to_smaster():
    with open(sys.argv[1], 'r') as f:
        content = f.read()

    content_dict = json.loads(content)
    headers = {'Content-Type': 'application/json'}
    cmd = {'num': 0, 'commands': []}
    num = 0
    for item in content_dict:
        num += 1
        item['uuid'] = str(uuid.uuid4())
        print item
        cmd['commands'].append(item)

    cmd['num'] = num
    response = requests.post('http://127.0.0.1:8082', data=json.dumps(cmd), headers=headers)
    return response


if __name__ == '__main__':
    #get_10_items()
    response = post_to_smaster()
