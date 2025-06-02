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

def bfs_search_for_keyword(start_url, keyword, max_pages=30):
    visited = set()
    queue = deque([[start_url]])
    count = 0
    last_path = []

    while queue and count < max_pages:
        path = queue.popleft()
        url = path[-1]

        if url in visited:
            continue

        visited.add(url)
        last_path = path  # Simpan path terakhir
        count += 1
        print(f"Visiting: {url}")

        try:
            response = requests.get(url, timeout=5)
            if keyword.lower() in response.text.lower():
                return {
                    "url": start_url,
                    "keyword": keyword,
                    "found": True,
                    "route": path
                }

            for link in get_links(url):
                if link not in visited:
                    queue.append(path + [link])

        except Exception as e:
            print(f"Error on {url}: {e}")
            continue

    # Kalau keyword tidak ditemukan, tetap kembalikan route terakhir
    return {
        "url": start_url,
        "keyword": keyword,
        "found": False,
        "route": last_path
    }
