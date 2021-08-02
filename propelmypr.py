from requests import Session
from utils import asf_data
from bs4 import BeautifulSoup
from copy import deepcopy
import pickle
from obj import (
    OutletResult,
    PitchingResult,
    JournalistResult,
    OutletSearchResult
)

host = 'https://app.propelmypr.com'
CLIENT_ID = "6m6c9u1ip7b2bmcs304orkek50"

class Propel(Session):
    def __init__(self, email=None, password=None) -> None:
        if email is None or password is None:
            print("ERROR: Please provide both email and password")
            exit()

        super().__init__()

        self.headers.update({
            'authority': 'app.propelmypr.com',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://app.propelmypr.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'en-US,en-IN;q=0.9,en;q=0.8'
        })

        try:
            cred_file = open(email + '.jar', 'rb')
            print('Credentials found!')
            cookies = pickle.load(cred_file)
            self.cookies.update(cookies)
            print("Credentials loaded!")
        except:
            print('No credentials found! Logging in...')
            self.get(host, allow_redirects=True)
            self.__login(email, password)
        finally:
            self.email = email
            self.password = password

    def __login(self, email, password):
        params = {
            'client_id': '6m6c9u1ip7b2bmcs304orkek50',
            'redirect_uri': 'https://app.propelmypr.com/app-public/after-login',
            'response_type': 'code',
            'scope': 'openid profile email',
            'nonce': '9740cbd478448167fc7185c5de627436c4qyKuRSU',
            'state': 'aef38a67976056ab0288b3821b0feaabb0N8sj751',
            'code_challenge': 'Mcm1TRkkrt2thxj8VDKRNBdhy8H_EPiJuIRL9mtc3m4',
            'code_challenge_method': 'S256',
        }
        headers = {
            'authority': 'login.propelmypr.com',
            'cache-control': 'max-age=0',
            'referer': 'https://app.propelmypr.com/',
        }

        self.get('https://login.propelmypr.com/oauth2/authorize', params=params)

        res = self.get('https://login.propelmypr.com/login', headers=headers, params=params)
        soup = BeautifulSoup(res.text, 'lxml')
        form = soup.find('form', { 'name': 'cognitoSignInForm' })
        _csrf = form.find('input', { 'name': '_csrf' })['value']
        asfData = asf_data(email, "", CLIENT_ID)

        login_data = {
            '_csrf': _csrf,
            'username': email,
            'password': password,
            'cognitoAsfData': asfData,
            'signInSubmitButton': 'Sign in'
        }
        res = self.post(host + form['action'], json=login_data, allow_redirects=True)
        with open(email + '.jar', 'wb') as cred_file:
            pickle.dump(res.cookies, cred_file)
            print("Login successful!")
        # driver = Chrome()
        # driver.get('https://app.propelmypr.com/')
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'signInFormUsername')))
        # form = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/form')
        # form.find_element_by_id('signInFormUsername').send_keys(email)
        # form.find_element_by_id('signInFormPassword').send_keys(password)
        # form.submit()
        # WebDriverWait(driver, 10).until(EC.url_contains('dashboard'))
        # cookies = driver.get_cookies()
        # for cookie in cookies:
        #     self.cookies.set(cookie['name'], cookie['value'])
        # with open(email + '.jar', 'wb') as cred_file:
        #     pickle.dump(self.cookies, cred_file)
        #     print("Login successful!")
        #     driver.quit()

    def ping(self):
        res = self.get('https://app.propelmypr.com/general/ping')

        if res.status_code == 401:
            print('Unauthorized! Trying to login again...')
            self.__login(self.email, self.password)
            print('Trying to fetch outlet again')
            return self.ping()
        else:
            return True

    def __extract(self, extract, _json, result={}, parent=None):
        keys = extract.keys()
        for k in keys:
            if type(extract[k]) is dict:
                if 'function' in extract[k]:
                    if parent is None:
                        parent = _json[k]
                    method = extract[k]['function']
                    result[extract[k]['_name']] = method(deepcopy(parent))

                    del extract[k]['_name']
                    del extract[k]['function']


                extractors = set(extract[k].keys())
                if len(extractors):
                    parent = _json[k]
                    print(type(parent), k)
                    r = self.__extract(extract=extract[k], _json=deepcopy(parent), result=result, parent=parent)
                    result.update(r)
            elif type(extract[k]) is str:
                try:
                    result[extract[k]] = parent[k]
                except: pass
        return deepcopy(result)

    def get_outlet_topics(self):
        res = self.get('https://app.propelmypr.com/media/getOutletTopics')
        if res.status_code == 401:
            print('Unauthorized! Trying to login again...')
            self.__login(self.email, self.password)
            print('Trying to fetch outlet again')
            return self.get_outlet_topics()
        return list(filter(None, res.json()['payload']))

    def get_journalist_topics(self):
        res = self.get('https://app.propelmypr.com/media/getJournalistTopics')
        if res.status_code == 401:
            print('Unauthorized! Trying to login again...')
            self.__login(self.email, self.password)
            print('Trying to fetch outlet again')
            return self.get_journalist_topics()
        return list(filter(None, res.json()['payload']))


    def get_outlet(self, outlet_id, extract=None) -> OutletResult:
        """
            extract = Key: Value pair
                key: result json object key string
                value: str|dict
                    str = value to store in csv column
                    dict = {
                        name: string to store in csv column,
                        fn(parent) -> any: method to execute for validation or computation
                    }
        """
        params = {
            'id': str(outlet_id)
        }

        res = self.get('https://app.propelmypr.com/media/getOutletWithMediaOutlet', params=params)
        if res.status_code == 401:
            print('Unauthorized! Trying to login again...')
            self.__login(self.email, self.password)
            print('Trying to fetch outlet again')
            return self.get_outlet(outlet_id=outlet_id, extract=extract)

        outlet_json = res.json()
        if extract:
            extracted_data = self.__extract(extract, outlet_json, result={}, parent=None)

        return OutletResult(outlet_json, extracted_data)

    def get_outlet_pitching(self, mediaOutletNameId, extract=None) -> PitchingResult:
        params = {
            'mediaOutletNameId': mediaOutletNameId
        }
        res = self.get('https://app.propelmypr.com/mediaOutlet/getOutletPitchingPreferences', params=params)

        if res.status_code == 401:
            print('Unauthorized! Trying to login again...')
            self.__login(self.email, self.password)
            print('Trying to fetch pitching again')
            return self.get_outlet_pitching(mediaOutletNameId=mediaOutletNameId, extract=extract)

        pitching_json = res.json()
        if extract:
            extracted_data = self.__extract(extract=extract, _json=pitching_json, result={}, parent=None)

        return PitchingResult(pitching_json, extracted_data)

    def get_journalist(self, journalist_id, extract=None) -> JournalistResult:
        params = {
            'id': journalist_id
        }

        res = self.get('https://app.propelmypr.com/media/getJournalist', params=params)

        if res.status_code == 401:
            print('Unauthorized! Trying to login again...')
            self.__login(self.email, self.password)
            print('Trying to fetch pitching again')
            return self.get_journalist(journalist_id=journalist_id, extract=extract)

        journalist_json = res.json()

        if extract:
            extracted_data = self.__extract(extract=extract, _json=journalist_json, result={}, parent=None)

        return JournalistResult(journalist_json, extracted_data)

    def get_journalist_pitching(self, journalist_email, extract=None) -> PitchingResult:
        params = {
            'email': journalist_email
        }

        res = self.get('https://app.propelmypr.com/contact/getContactPitchingPreferencesByEmail', params=params)

        if res.status_code == 401:
            print('Unauthorized! Trying to login again...')
            self.__login(self.email, self.password)
            print('Trying to fetch pitching again')
            return self.get_journalist_pitching(journalist_email=journalist_email, extract=extract)

        pitching_json = res.json()

        if extract:
            extracted_data = self.__extract(extract=extract, _json=pitching_json, result={}, parent=None)

        return PitchingResult(pitching_json, extracted_data)

    def search_outlets_by_topic(self, topics: list, query="", page=1, pageSize=51) -> OutletSearchResult:
        payload = {
            "q": query,
            "outletId": None,
            "advancedSearchFields": [
                {
                    "fieldKey": "topic",
                    "multiValue": True,
                    "operator": "EXACT_PHRASE",
                    "term": ",".join(topics)
                }
            ],
            "page": page,
            "pageSize": pageSize
        }
        res = self.post('https://app.propelmypr.com/media/searchOutlets', json=payload)
        return OutletSearchResult(res.json(), 'outlets')

    def search_journalists_by_topic(self, topics: list, query="", page=1, pageSize=51) -> OutletSearchResult:
        payload = {
            "q": query,
            "outletId": None,
            "advancedSearchFields": [
                {
                    "fieldKey": "topic",
                    "multiValue": True,
                    "operator": "EXACT_PHRASE",
                    "term": ",".join(topics)
                }
            ],
            "page": page,
            "pageSize": pageSize
        }
        res = self.post('https://app.propelmypr.com/media/searchJournalists', json=payload)
        return OutletSearchResult(res.json(), 'journalists')
