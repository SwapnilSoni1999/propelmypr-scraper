from requests import Session
from utils import asf_data
from bs4 import BeautifulSoup
import pickle

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
            with open(email + '.jar', 'rb') as cred_file:
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


    def ping(self):
        self.get('https://app.propelmypr.com/general/ping')

    def __extract(self, extract, _json, result={}, parent=None):
        keys = extract.keys()
        for k in keys:
            if type(extract[k]) is dict:
                if 'function' in extract[k]:
                    method = extract[k]['function']
                    result[extract[k]['_name']] = method(parent)

                    del extract[k]['_name']
                    del extract[k]['function']


                extractors = set(extract[k].keys())
                if len(extractors):
                    parent = _json[k]
                    r = self.__extract(extract=extract[k], _json=parent, result=result, parent=parent)
                    result.update(r)
            elif type(extract[k]) is str:
                result[extract[k]] = parent[k]
        return result


    def get_outlet(self, outlet_id, extract=None):
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
        if not extract:
            return res.json()
        else:
            return self.__extract(extract, res.json())
