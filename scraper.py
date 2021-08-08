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
import cache
from os import path
import math

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
        if pitching_data:
            outlet_data.extracted_data.update(pitching_data.extracted_data)
        return deepcopy(outlet_data.extracted_data)

    def run_task(self, ids: list, total: int):
        for outlet_id in ids:
            outlet_data = self.scrape_outlet(outlet_id)
            outlet_data = formatters.seperate_socials(outlet_data['Social Media Urls'], outlet_data)
            outlet_data = formatters.make_url(outlet_data, 'outlet')
            self.bus.put(outlet_data)
            print(f'{self.bus.qsize()}/{total}', 'Outletid', outlet_id, end='\r')

    def scrape(self):
        topics = pr.get_outlet_topics() #temp
        completed_topics = cache.get_topics('outlet')

        remaining_topics = list(set(topics).difference(set(completed_topics)))
        count = 1
        for topic in remaining_topics:
            topic = topic.replace('/', '_')
            if path.exists(f'outlet_{topic}.csv'):
                count+=1
                continue
            print("Scraping topic:", topic)
            print(f"> Count: {count}/{len(remaining_topics)}")
            res = pr.search_outlets_by_topic([topic])
            outlet_ids = list(map(lambda x: x['entity']['outletId'], res.data))
            outlet_ids = list(filter(None, outlet_ids))
            totalPages = res.totalPages
            if totalPages > 1:
                print(f"[{topic}] Total pages:", res.totalPages)
                for page_no in range(2, res.totalPages+1):
                    try:
                        print(f'[{topic}] Pages fetched:', f'{page_no}/{res.totalPages}', end='\r')
                        res = pr.search_outlets_by_topic([topic], page=page_no)
                        for idd in list(map(lambda x: x['entity']['outletId'], res.data)):
                            outlet_ids.append(idd)
                    except: continue
                print(f"[{topic}]Fetched all {totalPages} pages!")

            parts = math.ceil(len(outlet_ids)/THREADS)
            if parts == 0:
                parts = len(outlet_ids)
            chunks = utils.chunks(outlet_ids, parts or 1)
            threads = []
            for c in chunks:
                x = threading.Thread(target=self.run_task, args=(c, len(outlet_ids)))
                x.start()
                threads.append(x)
                time.sleep(1)

            for t in threads: t.join()

            final_data = []
            while not self.bus.empty():
                final_data.append(self.bus.get())
            utils.json_to_csv(fieldnames=final_data[0].keys(), data=final_data, filename=f'outlet_{topic}.csv')
            cache.checkpoint('outlet', topic)
            count += 1
            print(f'Saved Outlets to outlet_{topic}.csv!')

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

    def run_task(self, ids: list, total: int):
        for journalist_id in ids:
            journalist_data = self.scrape_journalist(journalist_id)
            journalist_data = formatters.seperate_socials(journalist_data['Social Media Urls'], journalist_data)
            journalist_data = formatters.make_url(journalist_data, 'journalist')
            self.bus.put(journalist_data)
            print(f'{self.bus.qsize()}/{total}', 'Journalist id:', journalist_id, end='\r')

    def scrape(self):
        pr.ping()
        completed_topics = cache.get_topics('journalist')
        topics = pr.get_journalist_topics()

        remaining_topics = list(set(topics).difference(set(completed_topics)))

        count = 1
        for topic in remaining_topics:
            topic = topic.replace('/', '_')
            if path.exists(f'journalist_{topic}.csv'):
                count+=1
                continue
            print("Scraping topic:", topic)
            print(f"> Count: {count}/{len(remaining_topics)}")
            res = pr.search_journalists_by_topic([topic])
            journalist_ids = list(map(lambda x: x['entity']['journalistId'], res.data))
            for page_no in range(2, res.totalPages+1):
                print(f'[{topic}]Pages fetched:', f'{page_no}/{res.totalPages}', end='\r')
                res = pr.search_outlets_by_topic([topic], page=page_no)
                for idd in list(map(lambda x: x['entity']['outletId'], res.data)):
                    journalist_ids.append(idd)
            print(f"[{topic}]Fetched all {res.totalPages} pages!")

            parts = int(len(journalist_ids)/THREADS)
            if parts == 0:
                parts = len(journalist_ids)
            chunks = utils.chunks(journalist_ids, parts)
            threads = []
            for c in chunks:
                x = threading.Thread(target=self.run_task, args=(c, len(journalist_ids)))
                x.start()
                threads.append(x)
                time.sleep(1)

            for t in threads: t.join()

            final_data = []
            while not self.bus.empty():
                final_data.append(self.bus.get())
            utils.json_to_csv(fieldnames=final_data[0].keys(), data=final_data, filename=f'journalist_{topic}.csv')
            cache.checkpoint('journalist', topic)
            count += 1
            print(f'Saved Journalists to journalist_{topic}.csv!')

if __name__ == '__main__':
    cache.load()
    print("Running threads:", THREADS)

    outlet = Outlet()
    journalist = Journalist()

    outlet.scrape()
    journalist.scrape()

