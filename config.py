from functions import (
    best_pitching_time,
    best_pitching_day,
    build_address,
    global_open_rate,
    global_response_rate,
    merge_socials,
    merge_topics,
)

THREADS = 100
CACHE_FILE = '.checkpoint'

outlet_config = {
    'payload': {
        'entity': {
            'outletId': 'Outlet ID',
            'journalistId': 'Journalist ID',
            'name': 'Name',
            'addressLine1': {
                'function': build_address,
                '_name': 'Address',
            },
            'state': 'State',
            'city': 'City',
            'country': 'Country',
            'phone': 'Phone Number',
            'email': 'Email Address',
            'topics': {
                'function': merge_topics,
                '_name': 'Topics'
            },
            'avatar': 'Image',
            'site': 'Website',
            'socials': {
                'function': merge_socials,
                '_name': 'Social Media Urls'
            }
        },
        'mediaOutlet': {
            'umv': 'Unique Monthly Visitors'
        },
    }
}

pitching_config = {
    'payload': {
        'numOpened': {
            'function': global_open_rate,
            '_name': 'Global Open Rate'
        },
        'numResponded': {
            'function': global_response_rate,
            '_name': 'Global Response Rate'
        },
        'numSent': 'Global Pitches Sent',
        'topics': {
            'function': merge_topics,
            '_name': 'Topics Most likely to get Response'
        },
        'dayOpenCounts': {
            'function': best_pitching_time,
            '_name': 'Best time to pitch'
        },
        'weekDayOpenCounts': {
            'function': best_pitching_day,
            '_name': 'Best day to pitch'
        }
    }
}
