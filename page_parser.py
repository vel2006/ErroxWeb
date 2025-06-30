from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from datetime import datetime
from requests import get

INFO_HEAD = "\033[92m[i]\033[0m "
MISC_HEAD = "\033[94m[*]\033[0m "
EROR_HEAD = "\033[91m[!]\033[0m "
IMPT_HEAD = "\033[33m[#]\033[0m "

class Parser():
    def __init__(self):
        self.site_contents = {}
    def add_page(self, url_to_add:str, verbose:bool=False):
        if verbose:
            print(f"{MISC_HEAD}Parsing: {url_to_add}")
        disable_warnings(InsecureRequestWarning)
        request = get(url_to_add, verify=False)
        if request.status_code == 200:
            data = request.content.decode(errors="ignore")
            self.site_contents[url_to_add] = [data, datetime.now().isoformat()]
    def get_parsed(self):
        return self.site_contents
