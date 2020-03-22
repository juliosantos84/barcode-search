import requests
import os
import json
import urllib.parse

class GoogleCustomSearch():
    def __init__(self, 
        apiKey = os.environ.get("GOOGLE_API_KEY"),
        searchEngineId = os.environ.get("GOOGLE_SEARCH_ENGINE_ID"),
        fileType = None, imgType = None):

        self._baseUrl = "https://www.googleapis.com/customsearch/v1"
        self._params = {
            "cx": searchEngineId, # Search Engine ID
            "key": apiKey,
        }

        if fileType:
            self._params["fileType"] = fileType

        if imgType:
            self._params["imgType"] = imgType

        self._headers = {
            "accept": "application/json"
        }

    def get_request_params(self, query=None, overrideParams=None):
        params = self._params.copy()
        
        if overrideParams:
            for key in overrideParams.keys():
                params[key] = overrideParams[key]
                if 'startIndex' in overrideParams:
                    params['start'] = overrideParams['startIndex']

        # Make the query url safe
        params['q'] = urllib.parse.quote_plus(query)
        params['searchTerms'] = params['q']
        return params
        

    def get_total_results(self, response=None):
        if response and 'searchInformation' in response:
            try:
                return int(response['searchInformation']['totalResults'])
            except KeyError:
                return 0

    def get_next_page(self, response=None):
        if response and 'queries' in response \
            and 'nextPage' in response['queries']:
            return response['queries']['nextPage'][0]
        else:
            return None

    def has_more_results(self, nextPage=None):
        return (nextPage and 'totalResults' in nextPage and int(nextPage['startIndex']) <= 100)

    def get_results(self, query=None, params=None, result_list=[]):
        params = self.get_request_params(query=query, overrideParams=params)
        r = requests.get(self._baseUrl, params=params, headers=self._headers)

        if r.status_code == 200:
            response = r.json()
            totalResults = self.get_total_results(response)

            for result in response['items']:
                result_list.append(result)

            nextPage = self.get_next_page(response)
            if self.has_more_results(nextPage):
                return self.get_results(query=query, params=nextPage, result_list=result_list)

        else:
            print ("Unable to get image urls. Got response %d from server"%(r.status_code))
            print (json.dumps(r.json()))
            r.raise_for_status()

        return result_list

