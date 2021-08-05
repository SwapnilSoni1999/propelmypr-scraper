from os import path
from config import CACHE_FILE
import json

cache_config = {
    'journalist': {
        'topics': []
    },
    'outlet': {
        'topics': []
    }
}

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def __create():
    json.dump(cache_config, open(CACHE_FILE, 'w'))
    print('Saved cache file!')

def load():
    if path.exists(CACHE_FILE) == False:
        print('Cache file doesnt exists! Creating new one...')
        __create()
    else:
        try:
            config = json.load(open(CACHE_FILE, 'r'))
            cache_config.update(config)
        except json.JSONDecodeError:
            __create()

def checkpoint(whom, topic):
    cache_config[whom]['topics'].append(topic)

def get_topics(entity):
    return cache_config[entity]['topics']
