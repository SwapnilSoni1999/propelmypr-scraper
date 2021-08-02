class PropelResult():
    def __init__(self, json, extracted_data=None) -> None:
        self.json = json
        self.extracted_data = extracted_data
        media_outlet = json['payload']['mediaOutlet']
        self.mediaOutletNameId = media_outlet['mediaOutletNameId']
        self.mediaOutletId = media_outlet['mediaOutletId']
        self.outletHashId = json['payload']['entity']['externalId']
