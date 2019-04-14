#!/usr/bin/env python3
import requests
import json
import time
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# globals
visited_links = []
links_to_visit = set()
set_depth = None
depth = 0
base_url = ''
site_map = {}
start_time = time.time()


def initialise(start_url: str, input_depth: int):
    global base_url, links_to_visit, set_depth
    try:
        parsed_url = urlparse(start_url)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc
        set_depth = int(input_depth)
        path = parsed_url.path or '/'
        links_to_visit.add(path)
        crawl()
    except (AttributeError, TypeError):
        print('that doesn\'t seem to be a url, please enter one :)')
        print('make sure to add the protocol to the url! (ie http or https)')
    except KeyboardInterrupt:
        print('\nInterrupted.')


def crawl():
    global links_to_visit, depth, visited_links, set_depth
    print('crawler working....')
    while len(links_to_visit) > 0 and depth is not set_depth:
        depth += 1
        next_link = links_to_visit.pop()
        all_fetched_links, filtered_links = fetch_links(next_link)
        add_to_site_map(next_link, all_fetched_links)
        links_to_visit = links_to_visit | set(filtered_links)

    print_sitemap()


def form_url(endpoint: str) -> str:
    global base_url
    path = endpoint if not endpoint.startswith('/') else base_url + endpoint
    return path


def parse_html_links(url: str) -> list:
    try:
        page = requests.get(url).content
        soup = BeautifulSoup(page, 'html.parser')
        link_tags = soup.findAll('a')
        all_hrefs = []
        for ref in link_tags:
            if ref.get('href') is None:
                # if a tag does not contain href
                continue
            # only add internal links (ie ones that start with /)
            # also remove mailto links
            if ref['href'].startswith('/') and 'email' not in ref['href']:
                all_hrefs.append(ref['href'])
        return all_hrefs
    except requests.exceptions.RequestException:
        # would handle bad request to retry
        return []


def filter_visited_links(all_links: list) -> list:
    global visited_links
    unvisited_links = [link for link in all_links if link not in visited_links]
    return unvisited_links


def fetch_links(endpoint: str) -> tuple:
    global visited_links
    if endpoint in visited_links:
        return [], []

    url = form_url(endpoint)
    all_links = parse_html_links(url)
    visited_links.append(endpoint)

    unvisited_links = filter_visited_links(all_links)
    return all_links, unvisited_links


def add_to_site_map(url: str, fetched_links: list):
    global site_map
    site_map[url] = fetched_links


def print_sitemap():
    global site_map, start_time, visited_links
    print(json.dumps(site_map, indent=2))
    end_time = time.time()
    duration = end_time - start_time
    print('-- webcrawler finished crawling --')
    print('crawled %d pages in %.1f seconds.' % (len(visited_links), duration))
    print('look in output.json for your sitemap')
    with open('output.json', 'w') as outfile:
        json.dump(site_map, outfile, indent=2)


def main():
    parser = argparse.ArgumentParser(description="a simple webcrawler. Pass in a url, get a sitelist back.")
    parser.add_argument('-u', help='the URL you want to crawl.')
    parser.add_argument('-d', help='the depth you want the crawler to go [optional]')
    parser.set_defaults(d=-1)
    args = parser.parse_args()
    initialise(args.u, args.d)

if __name__ == '__main__':
    main()
