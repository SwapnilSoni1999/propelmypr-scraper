import threading
from propelmypr import Propel
from config import (
    outlet_config,
    pitching_config,
    THREADS,
)
import formatters
import utils
from copy import deepcopy
import queue
import time

pr = Propel(email='marty@businessgrowthstrategist.com',
    password='G@ipUav6MoZp5!mGk5*9')

class Outlet:
    def __init__(self) -> None:
        bus = queue.Queue()
        self.bus = bus
        self.count = 1
        pr.ping()

    def scrape_outlet(self, outlet_id):
        outlet_data = pr.get_outlet(outlet_id, extract=deepcopy(outlet_config))
        pitching_data = pr.get_outlet_pitching(outlet_data.mediaOutletNameId, extract=deepcopy(pitching_config))
        outlet_data.extracted_data.update(pitching_data.extracted_data)
        return deepcopy(outlet_data.extracted_data)

    def run_task(self, ids: list):
        for outlet_id in ids:
            print(self.bus.qsize(), 'Outletid', outlet_id)
            outlet_data = self.scrape_outlet(outlet_id)
            outlet_data = formatters.seperate_socials(outlet_data['Social Media Urls'], outlet_data)
            outlet_data = formatters.make_url(outlet_data, 'outlet')
            self.bus.put_nowait(outlet_data)

    def scrape(self):
        topics = pr.get_outlet_topics() #temp
        res = pr.search_outlets_by_topic([topics[0]])
        outlet_ids = list(map(lambda x: x['entity']['outletId'], res.data)) #temporary now

        chunks = utils.chunks(outlet_ids, int(len(outlet_ids)/THREADS))
        threads = []
        for c in chunks:
            x = threading.Thread(target=self.run_task, args=(c,))
            x.start()
            threads.append(x)
            time.sleep(1)

        for t in threads: t.join()

        final_data = []
        while not self.bus.empty():
            final_data.append(self.bus.get())
        utils.json_to_csv(fieldnames=final_data[0].keys(), data=final_data, filename='outlet.csv')
        print('Saved Outlets to outlet.csv!')

class Journalist:
    def __init__(self) -> None:
        bus = queue.Queue()
        self.bus = bus
        self.count = 1
        pr.ping()

    def scrape_journalist(self, journalist_id):
        journalist_data = pr.get_journalist(journalist_id, extract=deepcopy(outlet_config))
        pitching_data = pr.get_journalist_pitching(journalist_data.email, extract=deepcopy(pitching_config))
        journalist_data.extracted_data.update(pitching_data.extracted_data)
        return deepcopy(journalist_data.extracted_data)

    def run_task(self, ids: list):
        for journalist_id in ids:
            print(self.bus.qsize(), 'Journalist id:', journalist_id)
            journalist_data = self.scrape_journalist(journalist_id)
            journalist_data = formatters.seperate_socials(journalist_data['Social Media Urls'], journalist_data)
            journalist_data = formatters.make_url(journalist_data, 'journalist')
            self.bus.put_nowait(journalist_data)

    def scrape(self):
        pr.ping()
        topics = pr.get_journalist_topics() # temporary
        res = pr.search_journalists_by_topic([topics[0]]) #for now first topic only
        journalist_ids = list(map(lambda x: x['entity']['journalistId'], res.data))

        chunks = utils.chunks(journalist_ids, int(len(journalist_ids)/THREADS))
        threads = []
        for c in chunks:
            x = threading.Thread(target=self.run_task, args=(c,))
            x.start()
            threads.append(x)
            time.sleep(1)

        for t in threads: t.join()

        final_data = []
        while not self.bus.empty():
            final_data.append(self.bus.get())
        utils.json_to_csv(fieldnames=final_data[0].keys(), data=final_data, filename='journalist.csv')
        print('Saved Journalists to journalist.csv!')

outlet = Outlet()
journalist = Journalist()

outlet.scrape()
journalist.scrape()

