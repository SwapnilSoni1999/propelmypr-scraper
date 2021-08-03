from functions import (
    best_pitching_time,
    best_pitching_day,
    build_address,
    global_open_rate,
    global_response_rate,
    merge_socials,
    merge_topics,
    build_url_outlet,
    build_url_journalist
)

outlet_config = {
    'payload': {
        'entity': {
            'outletId': {
                'function': build_url_outlet,
                '_name': 'Outlet URL'
            },
            'journalistId': {
                'function': build_url_journalist,
                '_name': 'Journalist URL'
            },
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

THREADS = 10

