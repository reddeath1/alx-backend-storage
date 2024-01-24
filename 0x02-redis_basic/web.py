#!/usr/bin/env python3
  """
   In this tasks, we will implement a get_page function (prototype: def get_page(url: str) -> str:). The core of the function is very simple. It uses the requests module to obtain the HTML content of a particular URL and returns it.
  """"
import requests
from functools import lru_cache
import time

@lru_cache(maxsize=None, typed=False)
def get_page(url):
    # Count the number of times the URL is accessed
    count_key = f"count:{url}"
    count = int(redis.get(count_key) or 0)
    redis.set(count_key, count + 1)

    # Check if the result is cached
    cached_result = redis.get(url)
    if cached_result:
        print(f"Cache hit for {url}")
        return cached_result.decode('utf-8')

    # Fetch the HTML content using requests
    response = requests.get(url)
    content = response.text

    # Cache the result with a 10-second expiration time
    redis.setex(url, 10, content)

    return content

if __name__ == "__main__":
    # Example usage
    redis = ...  # Initialize your Redis connection here

    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
    start_time = time.time()
    page_content = get_page(url)
    elapsed_time = time.time() - start_time

    print(f"URL: {url}")
    print(f"Content: {page_content}")
    print(f"Elapsed Time: {elapsed_time} seconds")
