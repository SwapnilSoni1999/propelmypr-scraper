import secrets
import random
import hmac
import hashlib
from base64 import b64encode
import json
from time import time
import csv

def code_verifier():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    randval = list(map(int, [secrets.randbits(8) for i in range(int((67-6)/2))]))
    return bytearray(randval).hex() + ''.join(random.choice(chars) for i in range(7))

def asf_data(username: str, user_poll_id: str, client_id: str):
    def signature(payload: dict, client_id: str, lib_version='JS20171115'):
        key = client_id.encode('utf-8')
        hm = hmac.new(key=key, digestmod=hashlib.sha256)
        hm.update(lib_version.encode('utf-8'))
        hm.update(json.dumps(payload).encode('utf-8'))
        return b64encode(hm.digest()).decode()

    def timestamp():
        return int(time() * 1000)


    lib_version = "JS20171115"
    payload = {
        "contextData": {
            "UserAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "DeviceId":"qn8ojaedcuyc9nnt228:1627189424942",
            "DeviceLanguage":"en-US",
            "DeviceFingerprint":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36Chrome PDF Plugin:Chrome PDF Viewer:Native Client:en-US",
            "DevicePlatform":"Linux x86_64",
            "ClientTimezone":".5:30"
        },
        "username": username,
        "userPoolId": user_poll_id,
        "timestamp": str(timestamp())
    }
    sign = signature(payload, client_id)

    asf = {
        "payload": json.dumps(payload),
        "signature": sign,
        "version": lib_version
    }
    return b64encode(json.dumps(asf).encode('utf-8')).decode()

def percentage(n, total):
    return "{:.2f}%".format((n/total) * 100)

class CsvHandler:
    def __init__(self, jsonKeys: list, filename) -> None:
        fp = open(filename, 'w')
        self.fp = fp
        writer = csv.writer(fp)
        self.writer = writer
        writer.writerow(jsonKeys)

    def close(self):
        self.fp.close()
