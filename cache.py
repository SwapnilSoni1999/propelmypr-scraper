from os import path
from config import CACHE_FILE
import pickle

cache_config = {
    'journalist': {
        'topics': set()
    },
    'outlet': {
        'topics': set()
    }
}

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def __create():
    pickle.dump(cache_config, open(CACHE_FILE, 'wb'))
    print('Saved cache file!')

def load():
    if path.exists(CACHE_FILE) == False:
        print('Cache file doesnt exists! Creating new one...')
        __create()
    else:
        config = pickle.load(open(CACHE_FILE, 'rb'))
        cache_config.update(config)

def checkpoint(whom, topic):
    cache_config[whom]['topics'].add(topic)

def get_topics(entity):
    return cache_config[entity]['topics']
