class StarWatchAPI:
    def __init__(self, apiurl, apikey, proxy):
        self.apiurl = apiurl
        self.apikey = apikey
        self.proxy = proxy
        self.headers = {"Authorization": "Bearer " + apikey}
        # Temporal
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_organizations(self):
        api_service = "organizations"
        response = requests.get(self.apiurl + api_service, verify=False, proxies=self.proxy, headers=self.headers)
        organizations_json = response.json()['organizations']
        organizations_json.sort(key=lambda x: x["id"])
        print(organizations_json)
