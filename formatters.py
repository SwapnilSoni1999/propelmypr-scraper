def seperate_socials(socials: str, parent: dict):
    urls = socials.split(',')
    del parent['Social Media Urls']
    social_keys = ['Linkedin', 'Twitter', 'Facebook', 'Instagram']
    for sk in social_keys:
        parent[sk] = None
    for url in urls:
        if 'linkedin' in url:
            parent['Linkedin'] = url
        if 'twitter' in url:
            parent['Twitter'] = url
        if 'facebook' in url:
            parent['Facebook'] = url
        if 'instagram' in url:
            parent['Instagram'] = url
    return parent

def make_url(data: dict, _type='outlet'):
    if _type == 'outlet':
        data['Outlet URL'] = 'https://app.propelmypr.com/app-media-db/outlets/' + str(data['Outlet ID'])
    elif _type == 'journalist':
        data['Journalist URL'] = 'https://app.propelmypr.com/app-media-db/journalists/' + str(data['Journalist ID'])
    return data
