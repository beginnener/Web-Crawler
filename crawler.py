# crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

def is_same_domain(base_url, target_url):
    return urlparse(base_url).netloc == urlparse(target_url).netloc

def get_links(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = urljoin(url, a_tag['href'])
            if is_same_domain(url, href):
                links.add(href)
        return links
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return set()

def bfs_crawl(start_url, max_pages=30):
    visited = set()
    queue = deque([start_url])
    route = []

    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        route.append(url)
        print(f"Visiting: {url}")

        for link in get_links(url):
            if link not in visited:
                queue.append(link)

    return {
        "url": start_url,
        "route": route
    }
