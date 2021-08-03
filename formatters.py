def seperate_socials(socials: str, parent: dict):
    urls = socials.split(',')
    del parent['Social Media Urls']
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
