import requests

class Anyside:
    def __init__(self,api_key):
        self.api_endpoint = "https://us-central1-test-anyside.cloudfunctions.net/api"
        self.api_key = api_key
        self.sess = requests.session()

    def query_domain(self,domain):
        try:
            response = self.sess.post(url=f"{self.api_endpoint}/public/queryDomain",json={"domain":domain,"api_key":self.api_key})
            return response.json()
        except Exception:
            return {"message":"Error"}

    def lookup_wallet(self,wallet_address):
        try:
            response = self.sess.post(url=f"{self.api_endpoint}/public/lookupWallet",json={"wallet_address":wallet_address,"api_key":self.api_key})
            return response.json()
        except Exception:
            return {"message":"Error"}