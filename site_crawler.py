from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from random import randint
from requests import get
from time import sleep
from re import findall

# Defining print headers
INFO_HEAD = "\033[92m[i]\033[0m "
MISC_HEAD = "\033[94m[*]\033[0m "
EROR_HEAD = "\033[91m[!]\033[0m "
IMPT_HEAD = "\033[33m[#]\033[0m "

# Defining regex patterns
a_href_regex = r"<a href=\"([^\"]+)\">"
img_regex = r"<img src=\"([^\"]+)\""
javascript_file_regex = r"<script type=\"text/javascript\"\D+src=\"([^\"]+)\">"
javascript_imbeded_regex = r"<script type=\"text/javascript\">(.*?)</script>"
javascript_embeded_file_regex1 = r"src=\'(.*?)\';"
javascript_embeded_file_regex2 = r"src=\\\'(.*?)\\\';"
javascript_embeded_file_regex3 = r"https?://(?:www\.)?([^\"\']+)"
domain_regex = r"https?://(?:www\.)?([^\"/]+)"

class RefrenceCrawler():
    def __init__(self, starting_page=str):
        disable_warnings(category=InsecureRequestWarning)
        self.buffer = [starting_page]
        self.found  = set()
        self.run = True
    def crawl(self, verbose:bool=False):
        while self.run and self.buffer:
            if self.buffer[0] in self.found:
                self.buffer.pop(0)
                continue
            else:
                if verbose:
                    print(f"{INFO_HEAD}Attempting page: {self.buffer[0]}")
                request = get(self.buffer[0], verify=False)
                if request.status_code == 200:
                    self.found.add(self.buffer[0])
                    if verbose:
                        print(f"{MISC_HEAD}Searching for links...")
                    domain = findall(domain_regex, self.buffer[0])
                    page_data = request.content.decode()

                    # Searching for page links
                    links = findall(a_href_regex, page_data)
                    for link in links:
                        page = ""
                        if link[0] == "/":
                            page = f"https://{domain[0]}{link}"
                        else:
                            continue
                        if page not in self.found and page not in self.buffer:
                            if verbose:
                                print(f"{MISC_HEAD}Found link: {page}")
                            self.buffer.append(page)

                    # Searching for image refrences
                    images = findall(img_regex, page_data)
                    for image in images:
                        page = ""
                        if image[0] == "/":
                            page = f"https://{domain[0]}{image}"
                        else:
                            continue
                        if page not in self.found:
                            if verbose:
                                print(f"{MISC_HEAD}Found image: {page}")
                            self.found.add(page)

                    # Searching for javascript file refrences
                    javascripts = findall(javascript_file_regex, page_data)
                    for script in javascripts:
                        page = ""
                        if script[0] == "/":
                            page = f"https://{domain[0]}{script}"
                        else:
                            continue
                        if page not in self.found:
                            if verbose:
                                print(f"{MISC_HEAD}Found javascript file: {page}")
                            self.found.add(page)

                    # Searching for javascript file refrences within code
                    javascripts = findall(javascript_imbeded_regex, page_data)
                    for script in javascripts:
                        scripts = findall(javascript_embeded_file_regex1, script)
                        for script2 in scripts:
                            if script2 not in self.buffer and script2 not in self.found:
                                if verbose:
                                    print(f"{MISC_HEAD}Found javascript file refrence: {script2}")
                                self.buffer.append(f"{script2}")
                        scripts = findall(javascript_embeded_file_regex2, script)
                        for script2 in scripts:
                            page = f"https://{script2}"
                            if page not in self.buffer and page not in self.found:
                                if verbose:
                                    print(f"{MISC_HEAD}Found javascript file refrence: {page}")
                                self.buffer.append(f"https://{script2}")
                        scripts = findall(javascript_embeded_file_regex3, script)
                        for script2 in scripts:
                            page = f"https://{script2}"
                            if page not in self.buffer and page not in self.found:
                                if verbose:
                                    print(f"{MISC_HEAD}Found javascript file refrence: {page}")
                                self.buffer.append(page)

                    # Searching for direct javascript file refrences
                    javascripts = findall(javascript_embeded_file_regex3, page_data)
                    for script in javascripts:
                        if ".js" in script:
                            page = f"https://{script}"
                            if verbose:
                                print(f"{MISC_HEAD}Found linked javascript file: {page}")
                            self.buffer.append(page)
                    self.found.add(self.buffer[0])
                    sleep(randint(1, 3))
                else:
                    if verbose:
                        print(f"{EROR_HEAD}Failed to get page: {self.buffer[0]} ({request.status_code})")
                self.buffer.pop(0)
    def get_pages(self):
        return self.found
    def stop(self):
        self.run = False
