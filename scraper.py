from propelmypr import Propel
from config import (
    outlet_config,
    pitching_config
)
import utils
from copy import deepcopy

pr = Propel(email='marty@businessgrowthstrategist.com',
    password='G@ipUav6MoZp5!mGk5*9')


def scrape_outlet(outlet_id):
    outlet_data = pr.get_outlet(outlet_id, extract=deepcopy(outlet_config))
    pitching_data = pr.get_outlet_pitching(outlet_data.mediaOutletNameId, extract=deepcopy(pitching_config))
    outlet_data.extracted_data.update(pitching_data.extracted_data)
    return deepcopy(outlet_data.extracted_data)

def scrape_journalist(journalist_id):
    journalist_data = pr.get_journalist(journalist_id, extract=deepcopy(outlet_config))
    pitching_data = pr.get_journalist_pitching(journalist_data.email, extract=deepcopy(pitching_config))
    journalist_data.extracted_data.update(pitching_data.extracted_data)
    return deepcopy(journalist_data.extracted_data)

def fetch_all_outlets():
    pr.ping()
    topics = pr.get_outlet_topics() #temp
    res = pr.search_outlets_by_topic([topics[0]])
    outlet_ids = list(map(lambda x: x['entity']['outletId'], res.data))
    final_data = []
    count = 1
    for outlet_id in outlet_ids:
        print(count, 'Outletid', outlet_id)
        outlet_data = scrape_outlet(outlet_id)
        final_data.append(outlet_data)
        count += 1

    print(final_data)
    utils.json_to_csv(fieldnames=final_data[0].keys(), data=final_data, filename='outlet.csv')

def fetch_all_journalists():
    pr.ping()
    topics = pr.get_journalist_topics() # temporary
    res = pr.search_journalists_by_topic([topics[0]])
    journalist_ids = list(map(lambda x: x['entity']['journalistId'], res.data))
    final_data = []
    count = 1
    for journalist_id in journalist_ids:
        print(count, 'Journalist id:', journalist_id)
        journalist_data = scrape_journalist(journalist_id)
        final_data.append(journalist_data)
        count += 1

    utils.json_to_csv(fieldnames=final_data[0].keys(), data=final_data, filename='journalist.csv')

fetch_all_outlets()
fetch_all_journalists()