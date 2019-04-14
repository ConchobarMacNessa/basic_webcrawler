# WebCrawler

# Contents
 - [Introduction](#introduction)
 - [Running the Webcrawler](#running)
 - [Testing](#testing)
 - [Notes](#notes)
 
# Introduction

This webcrawler is a simple crawler designed to return a sitemap of internal links. While not complete, this webcrawler should work with most sites.

# Running

### Before Running the Crawler
Before running this crawler, ensure you have installed the correct dependencies by navigating to this folder and installing the requirements.txt with `pip install -r requirements.txt`

## Running the Webcrawler
This project is run by executing the executable python file `crawler.py`, which takes in a url with `-u` and an optional depth with `-u`.
An example of running this is run the following command in this directory:
`./crawler.py -u 'https://monzo.com' -d 5`

After this has finished running, it will print out the sitemap in the terminal - however, a lot of sites will produce a huge sitemap, which might not all be visible in the terminal. To overcome this, the sitemap will also be written into the `output.json` file in this directory. This will be overwritten every time you generate a new sitemap.

Note that from the terminal you can also run `./crawler.py -h` to see usage for the crawler.

## Using Depth
Note, that if a site is very big and you don't want to crawl its entirety (It might take quite a while to crawl the whole of wikipedia, for example...), there is an optional depth argument, passed into the programme with the `-d` flag. This sets the limit to how many levels you want to want to crawl.

# Testing

There are unit tests for this crawler, which can be executed with: `python crawlerTest.py`

# Notes

This is by no means a finished crawlers, and there are a few things to note:
1. This webcrawler will make a request to the url to get the html to parse for each site. At the moment, if the request is unsuccessful, it will simply return an empty array of links for that site - if I were to have more time, I would impliment a retry system and at the very least better error handling in the event of a bad request.
2. The webcrawler is quite brittle - if you pass in an initial site without http(s) if will not work. I would like to provide better url handling.
3. For a semi large site, this webcrawler will take a long time - had I more time I would have implimented concurrency to take this time down.

