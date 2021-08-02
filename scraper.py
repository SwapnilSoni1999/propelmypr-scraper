from propelmypr import Propel
from config import (
    outlet_config,
    pitching_config
)
import utils

pr = Propel(email='marty@businessgrowthstrategist.com',
    password='G@ipUav6MoZp5!mGk5*9')


def scrape_outlet(outlet_id):
    outlet_data = pr.get_outlet(outlet_id, extract=outlet_config)
    pitching_data = pr.get_outlet_pitching(outlet_data.mediaOutletNameId, extract=pitching_config)
    outlet_data.extracted_data.update(pitching_data.extracted_data)
    return outlet_data.extracted_data

def scrape_journalist(journalist_id):
    journalist_data = pr.get_journalist(journalist_id, extract=outlet_config)
    pitching_data = pr.get_journalist_pitching(journalist_data.email, extract=pitching_config)
    journalist_data.extracted_data.update(pitching_data.extracted_data)
    return journalist_data.extracted_data

outlet_data = scrape_outlet(225716)
journalist_data = scrape_journalist(95908)

outlet_csv = utils.CsvHandler(outlet_data.keys(), 'outlet.csv')
journalist_csv = utils.CsvHandler(journalist_data.keys(), 'journalist.csv')

outlet_csv.writer.writerow(outlet_data.values())
journalist_csv.writer.writerow(journalist_data.values())

outlet_csv.close()
journalist_csv.close()