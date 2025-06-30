# ErroxWeb

## Description:

A site crawler, designed to find any linked or refrenced pages

## Usage:

To use this project, simply run the main.py file with the wanted arguments, those can be found by using the -h flag (or looking below)

### arguments:

 -s | Crawl any found subdomains

 -d | save / download any found pages or files
 
 -v | verbose, print out every operation

### example:

Windows:

python main.py https://vel2006.github.io/ -v -d

Linux:

python3 main.py https://vel2006.github.io/ -v -d

## Explination:

### main.py

main.py holds the connecting logic of the other scripts. It works by first testing to see if the target site / page is online through a HTTP GET request, if the response code is 200 then the script continues. While single threaded, it can easily crawl a thirty page site within a few moments. Once all the pages are collected they are parsed (if selected) and saved to disk into the file "found_items.json".

### site_crawler.py

site_crawler.py works by taking in a starting page, then looping through all found links or refrences on each page. It does this by examining the response from a HTTP GET request, it will try to find any images, pages, or javascript files. If any are found they are saved in a buffer to be requested later.

### page_parser.py

page_parser.py works by requesting the wanted page, then saving the decoded output so it can be written to disk.
