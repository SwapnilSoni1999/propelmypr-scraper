import utils

def build_address(parent):
        ret = ''
        k1 = 'addressLine1'
        k2 = 'addressLine2'
        if parent[k1]:
            ret += parent[k1]
        if parent[k2]:
            ret += parent[k2]
        return ret

def merge_topics(parent):
    return ','.join(parent['topics'])

def merge_socials(parent):
    return ','.join(list(map(lambda x: x['url'], parent['socials'])))

def global_open_rate(parent):
        total = parent['numSent']
        n = parent['numOpened']
        return utils.percentage(n, total)

def global_response_rate(parent):
    total = parent['numSent']
    n = parent['numResponded']
    return utils.percentage(n, total)

def best_pitching_time(parent):
    times = parent['dayOpenCounts']
    max_val = max(times.values())
    for key, val in times.items():
        if val == max_val:
            return key

def best_pitching_day(parent):
    days = parent['weekDayOpenCounts']
    max_val = max(days.values())
    for key, val in days.items():
        if val == max_val:
            return key
