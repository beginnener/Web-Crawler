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

# DFS
def crawl_dfs(url, visited=None, depth=0):
    if visited is None:
        visited = set()

    if url in visited:
        return visited

    visited.add(url)
    print("  " * depth + f"DFS visiting: {url}")

    for link in get_links(url):
        crawl_dfs(link, visited, depth + 1)

    return visited

# BFS
def crawl_bfs(start_url):
    visited = set()
    queue = deque([start_url])

    while queue:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        print(f"BFS visiting: {url}")
        for link in get_links(url):
            if link not in visited:
                queue.append(link)

    return visited

# Antarmuka pengguna
def main():
    print("=== SIMPLE SEARCH ENGINE CRAWLER ===")
    start_url = input("Masukkan URL awal (misal: https://example.com): ").strip()

    if not start_url.startswith("http"):
        start_url = "https://" + start_url

    method = input("Pilih metode crawling (dfs/bfs): ").lower()
    print(f"\nMemulai crawling dengan metode {method.upper()}...\n")

    if method == "dfs":
        crawl_dfs(start_url)
    elif method == "bfs":
        crawl_bfs(start_url)
    else:
        print("Metode tidak dikenali. Gunakan 'dfs' atau 'bfs'.")

if __name__ == "__main__":
    main()
