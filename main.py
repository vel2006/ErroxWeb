from urllib3.exceptions import InsecureRequestWarning
from site_crawler import RefrenceCrawler
from platform import system as platform
from urllib3 import disable_warnings
from argparse import ArgumentParser
from page_parser import Parser
from random import randint
from requests import get
from time import sleep
from re import findall
from os import system
from json import dump

# Welcome art stuffs
if platform().lower() == "windows":
    system("cls")
else:
    system("clear")
print(" _____                   __        __   _     ")
print("| ____|_ __ _ __ _____  _\\ \\      / /__| |__  ")
print("|  _| | '__| '__/ _ \\ \\/ /\\ \\ /\\ / / _ \\ '_ \\ ")
print("| |___| |  | | | (_) >  <  \\ V  V /  __/ |_) |")
print("|_____|_|  |_|  \\___/_/\\_\\  \\_/\\_/ \\___|_.__/")
print("Version: 3.0")
print("\nProgramed by: That1EthicalHacker\nYoutube: @That1EthicalHacker\nGitHub: https://github.com/vel2006")

# Defining global variables
INFO_HEAD = "\033[92m[i]\033[0m "
MISC_HEAD = "\033[94m[*]\033[0m "
EROR_HEAD = "\033[91m[!]\033[0m "
IMPT_HEAD = "\033[33m[#]\033[0m "
domain_regex = r"https?://(?:www\.)?([^\"/]+)"
domain_data = []

# Collecting arguments
print(f"{IMPT_HEAD}Parsing arguments")
parser = ArgumentParser(
    prog="ErroxWeb",
    description="A basic website crawler and page discovery tool.",
    epilog="Programed by: That1EthicalHacker.",
    usage="%(prog)s domain [options]"
)
parser.add_argument("target_site", help="Target domain to crawl, ex: https://vel2006.github.io")
parser.add_argument("-s", "--crawl_subdomains", action="store_true", help="Crawl subdomains of the site")
parser.add_argument("-v", "--verbose", action="store_true", help="Print out all found items and current actions")
parser.add_argument("-d", "--download_pages", action="store_true", help="Download / save data of each found web page, image and javascript file. Warning: This will take roughly as long as crawling does.")
args = parser.parse_args()
target_site = args.target_site

# Formating the target site url
if target_site.startswith("https://"):
    pass
else:
    print(f"{EROR_HEAD}Target site: \"{target_site}\" MUST be https based.")
    exit()
if not target_site.endswith("/"):
    print(f"{EROR_HEAD}Target site: \"{target_site}\" MUST end with \"/\".")
    exit()

# Checking the site's availability
disable_warnings(category=InsecureRequestWarning)
if get(target_site, verify=False).status_code != 200:
    print(f"{EROR_HEAD}Target site: \"{target_site}\" did not return 200 to a GET request.")
    exit()

# Refrence crawling the site
site_domain = findall(domain_regex, target_site)[0]
print(f"{IMPT_HEAD}Crawling target site: {site_domain}")
crawler = RefrenceCrawler(target_site)
crawler.crawl(args.verbose)
found_data = crawler.get_pages()
for item in found_data:
    domain_data.append(item)
if args.verbose:
    print(f"{INFO_HEAD}Found {len(domain_data)} web pages, images or javascript files")

# Getting subdomains
subdomains = [""]
tries = 0
print(f"{IMPT_HEAD}Finding subdomains through crt.sh for site: {site_domain}")
while True:
    response = get(f"https://crt.sh/?q={site_domain}&output=json")
    if response.status_code == 200:
        if response.content.decode():
            try:
                for key, value in enumerate(response.json()):
                    if "\n" not in value['name_value']:
                        subdomains.append(value['name_value'])
                subdomains = sorted(set(subdomains))
                break
            except Exception:
                pass
    elif response.status_code != 502 and response.status_code != 503:
        if args.verbose:
            print(f"{EROR_HEAD}Unknown response from crt.sh, assuming failure.")
        break
    if tries == 2:
        if args.verbose:
            print(f"{EROR_HEAD}crt.sh returned nothing, 503 or 502, max attempts reached, assuming failure.")
        break
    if args.verbose:
        print(f"{EROR_HEAD}crt.sh returned nothing, 503 or 502 error, trying again in ten seconds... ({2 - tries} attempts remaining)")
    sleep(10)
    tries += 1
subdomains.remove("")

# Crawling subdomains
if subdomains == []:
    if args.verbose:
        print(f"{INFO_HEAD}Did not find any subdomains.")
else:
    print(f"{INFO_HEAD}Found {len(subdomains)} subdomains for site: {site_domain}")
    if args.crawl_subdomains:
        for subdomain in subdomains:
            if args.verbose:
                print(f"{IMPT_HEAD}Starting crawl on: {subdomain}")
            sub_crawler = RefrenceCrawler(f"https://{subdomain}")
            sub_crawler.crawl(args.verbose)
            items = sub_crawler.get_pages()
            if args.verbose:
                print(f"{INFO_HEAD}Found {len(items)} in subdomain: {subdomain}")
            for item in items:
                domain_data.append(item)
    if args.verbose:
        print(f"{IMPT_HEAD}Found {len(domain_data) - len(found_data)} items in subdomains")

# Downloading the pages for saving contents
output_data = {}
print(f"{IMPT_HEAD}Parsing found files in crawling")
if args.download_pages:
    parser = Parser()
    for item in domain_data:
        parser.add_page(item, args.verbose)
        sleep(randint(1, 3))
    output_data = parser.get_parsed()
else:
    for item in domain_data:
        output_data[item] = "Didn\'t save file\'s contents."

# Saving all found files
print(f"{IMPT_HEAD}Saving all found data in file \"found_items.json\"")
with open("found_items.json", "w") as file_handle:
    dump(output_data, file_handle, indent=4)
    file_handle.close()
