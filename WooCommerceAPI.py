import requests
import json
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError, ConnectionError, Timeout

class WooCommerceAPI:
    def __init__(self, url, consumer_key, consumer_secret, timeout=10, max_retries=3):
        self.url = url.rstrip('/')
        self.auth = (consumer_key, consumer_secret)
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = timeout
        self.max_retries = max_retries
    
    def _request(self, method, endpoint, data=None, params=None):
        url = f"{self.url}/wp-json/wc/v3/{endpoint}"
        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method,
                    url,
                    auth=self.auth,
                    headers=self.headers,
                    timeout=self.timeout,
                    data=json.dumps(data) if data else None,
                    params=params
                )
                response.raise_for_status()
                response.encoding = 'utf-8'  # اطمینان از کدگذاری صحیح
                return response.json()
            except (HTTPError, ConnectionError, Timeout) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt + 1 == self.max_retries:
                    raise Exception(f"API request failed after {self.max_retries} attempts")
    
    
    def get(self, endpoint, params=None):
        return self._request("GET", endpoint, params=params)
    
    def post(self, endpoint, data):
        return self._request("POST", endpoint, data)
    
    def put(self, endpoint, data):
        return self._request("PUT", endpoint, data)
    
    def delete(self, endpoint):
        return self._request("DELETE", endpoint)
    
    def get_all_products(self, per_page=100):
        products = []
        page = 1
        while True:
            params = {'per_page': per_page, 'page': page}
            page_products = self.get("products", params=params)
            if not page_products:
                break
            products.extend(page_products)
            page += 1
        return products
    
    def get_products(self):
        return self.get("products")
    

    def create_product(self, product_data):
        return self.post("products", product_data)
    
    def update_product(self, product_id, product_data):
        return self.put(f"products/{product_id}", product_data)
    
    def delete_product(self, product_id, force=True):
        return self.delete(f"products/{product_id}?force={str(force).lower()}")


