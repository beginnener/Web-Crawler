import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import json
import mysql.connector

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

def save_crawl_result(seed_url, keyword, route, found):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # ubah jika pakai password
        database='crawler_db'
    )
    cursor = conn.cursor()

    visited_json = json.dumps(route)
    found_json = json.dumps([route[-1]] if found else [])

    cursor.execute('''
        INSERT INTO crawl_results (seed_url, keyword, visited_urls, found_urls)
        VALUES (%s, %s, %s, %s)
    ''', (seed_url, keyword, visited_json, found_json))

    conn.commit()
    conn.close()

def dfs_search_for_keyword_and_save(start_url, keyword, max_pages=30, max_depth=3):
    visited = set()
    result_count = 0
    found_routes = []

    def dfs(current_url, path, depth):
        nonlocal result_count

        if result_count >= max_pages or depth > max_depth:
            return

        if current_url in visited:
            return

        visited.add(current_url)
        print("  " * depth + f"DFS visiting: {current_url}")

        try:
            response = requests.get(current_url, timeout=5)
            if keyword.lower() in response.text.lower():
                found_routes.append(path[:])

                # Cek dan hapus jika duplikat
                visited_json = json.dumps(path[:])
                found_json = json.dumps([path[-1]])

                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='crawler_db'
                )
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM crawl_results
                    WHERE seed_url = %s AND keyword = %s AND visited_urls = %s AND found_urls = %s
                ''', (start_url, keyword, visited_json, found_json))
                conn.commit()
                conn.close()

                save_crawl_result(start_url, keyword, path[:], True)
                result_count += 1
        except Exception as e:
            print(f"Error on {current_url}: {e}")
            return

        for link in get_links(current_url):
            if link not in visited:
                dfs(link, path + [link], depth + 1)

    dfs(start_url, [start_url], 0)

    return [
        {
            "url": start_url,
            "keyword": keyword,
            "found": True,
            "route": route,
            "found_in": [route[-1]]
        }
        for route in found_routes
    ]
