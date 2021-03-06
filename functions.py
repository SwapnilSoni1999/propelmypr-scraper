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
    try:
        return ','.join(parent['topics'])
    except:
        return None

def merge_socials(parent):
    return ','.join(list(map(lambda x: x['url'], parent['socials'])))

def global_open_rate(parent):
    try:
        total = parent['numSent']
        n = parent['numOpened']
        return utils.percentage(n, total)
    except: return None

def global_response_rate(parent):
    try:
        total = parent['numSent']
        n = parent['numResponded']
        return utils.percentage(n, total)
    except: return None

def best_pitching_time(parent):
    try:
        times = parent['dayOpenCounts']
        max_val = max(times.values())
        for key, val in times.items():
            if val == max_val:
                return key
    except: return None

def best_pitching_day(parent):
    try:
        days = parent['weekDayOpenCounts']
        max_val = max(days.values())
        for key, val in days.items():
            if val == max_val:
                return key
    except: return None
