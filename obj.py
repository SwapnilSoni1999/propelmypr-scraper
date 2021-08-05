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
        try:
            self.data = json['payload'][key]
            self.totalPages = math.ceil(json['payload']['total'] / pageSize)
            self.total = json['payload']['total']
        except:
            print("\n\n===========")
            print(json)