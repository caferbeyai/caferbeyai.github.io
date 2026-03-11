#!/usr/bin/env python3
"""Simple news fetcher - outputs news in structured format."""

import json

# URLs to fetch
URLS = {
    "nos": "https://nos.nl/nieuws/laatste",
    "bbc": "https://www.bbc.com/news/world",
    "reuters": "https://www.reuters.com/world/",
    "cnn": "https://www.cnn.com/world"
}

if __name__ == "__main__":
    print(json.dumps(URLS, indent=2))
    print("\n# Use web_fetch tool to get news content")
