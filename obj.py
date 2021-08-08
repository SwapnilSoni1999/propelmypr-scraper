import math
class OutletResult():
    def __init__(self, json, extracted_data=None) -> None:
        self.json = json
        self.extracted_data = extracted_data
        media_outlet = json['payload']['mediaOutlet']
        self.mediaOutletNameId = media_outlet['mediaOutletNameId']
        self.mediaOutletId = media_outlet['mediaOutletId']
        self.outletHashId = json['payload']['entity']['externalId']

class PitchingResult():
    def __init__(self, json, extracted_data=None) -> None:
        self.json = json
        self.extracted_data = extracted_data

class JournalistResult():
    def __init__(self, json, extracted_data=None) -> None:
        self.json = json
        self.extracted_data = extracted_data
        self.email = json['payload']['entity']['email']

class SearchResult():
    def __init__(self, json, key, pageSize) -> None:
        self.data = json['payload'][key]
        self.totalPages = math.ceil(self.calculate_total(json['payload']['facets']['country']))
        self.total = json['payload']['total']

    def calculate_total(self, countries):
        count = 0
        for c in countries: count += c['count']
        return count
