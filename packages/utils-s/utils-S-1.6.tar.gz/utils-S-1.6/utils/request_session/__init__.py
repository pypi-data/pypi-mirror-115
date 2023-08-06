import requests
class requests_session:
    def __init__(self):
        self.ses = requests.Session()

    def get(self, url, Head=None):
        if Head is not None:
            return self.ses.get(url, headers=Head)
        else:
            return self.ses.get(url)

    def post(self, url, data=None, json=None, headers=None):
        return self.ses.post(url=url, data=data, json=json, headers=headers)

    def session(self):
        return self.ses


    def request(self, method, url, params=None, data=None, headers=None,
            cookies=None, files=None, auth=None, timeout=None,
            allow_redirects=True, proxies=None,
            hooks=None,verify=None,
            json=None):

        return self.ses.request(url=url,method=method, proxies=proxies,
                                params=params, data=data, headers=headers,
                                cookies=cookies, files=files, auth=auth, timeout=timeout,
                                allow_redirects=allow_redirects, hooks=hooks, verify=verify, json=json)

def waste():
    pass