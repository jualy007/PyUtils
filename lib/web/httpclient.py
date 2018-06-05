# coding=utf-8

import http.client
import json
import traceback
import urllib.parse

from lib.log import Log


class HttpClient():
    type = ('OPTIONS', 'HEAD', 'GET', 'POST', 'PUT', 'DELETE', 'TRACE')

    headers = {
        "Accept": "application/json",
        "Accept - Encoding": "gzip, deflate",
        "Connection": "keep - alive",
        "Content-Type": "application/json"
    }

    def __init__(self, host, port=None):
        self.logger = Log(__name__)
        self.host = host
        self.port = port if port else 80

    def request(self, requestType, urlPath, params, headers):
        results = []

        con = http.client.HTTPConnection(self.host)
        try:
            if requestType.upper() not in self.type:
                raise Exception

            params = urllib.parse.urlencode(params)
            con.request(requestType.upper(), urlPath, params, headers)
            resu = con.getresponse()
            results.append(resu.status)
            results.append(resu.read())
            resu.close()
        except:
            self.logger.error("Request Execute Failed")
            traceback.print_exc()
        finally:
            con.close()

        if results[0] == 200:
            if isinstance(results[1], bytes) and results[1].__len__() >= 1:
                results = json.loads(results[1].decode('utf-8'))
            elif results[1].__len__() >= 1:
                results = json.loads(results[1])
            else:
                results = "Succeed"
        else:
            self.logger.error(
                "ERROR!!! Request {0} execute failed!!!".format(urlPath))
            results = None

        return results

    def requestWithJSON(self, requestType, urlPath, params, headers):
        results = []

        con = http.client.HTTPConnection(self.host)
        try:
            if requestType.upper() not in self.type:
                raise Exception

            con.request(requestType.upper(), urlPath, json.dumps(params),
                        headers)
            resu = con.getresponse()
            self.logger.info(resu.reason)
            results.append(resu.status)
            results.append(resu.read())
            resu.close()
        except:
            self.logger.error("Request Execute Failed")
        finally:
            con.close()

        if results[0] == 200:
            if isinstance(results[1], bytes):
                results = json.loads(results[1].decode('utf-8'))
            else:
                results = json.loads(results[1])
        else:
            self.logger.error(
                "ERROR!!! Request {0} execute failed!!!".format(urlPath))
            results = None

        return results
