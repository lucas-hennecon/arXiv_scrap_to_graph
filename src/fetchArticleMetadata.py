"""
Function that retrieves arXiv article metadata.
"""

import requests
import xml.etree.ElementTree as ET
import time


def fetch_arxiv_metadata(arxiv_query: str) -> dict:
    """
    Fetches metadata from the ArXiv API.
    :param arxiv_query: The ArXiv query, e.g., "id:1805.08355"
    :return: A dictionary containing metadata for the paper.
    """
    base_url = "http://export.arxiv.org/api/query"
    retries = 3  # Number of retries for failed requests
    for attempt in range(retries):
        try:
            # Make the API request
            response = requests.get(base_url, params={"search_query": arxiv_query, "max_results": 1}, timeout=10)
            
            # Check for HTTP errors
            if response.status_code != 200:
                print(f"ArXiv API request failed with status {response.status_code}, retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            
            # Parse the XML response
            root = ET.fromstring(response.text)
            entry = root.find("{http://www.w3.org/2005/Atom}entry")

            if entry is None:
                print(f"No entry found in the ArXiv response for query {arxiv_query}")
                return {
                    "title": "Unknown Title",
                    "authors": [],
                    "published": "0000-00-00T00:00:00Z",
                    "link": ""
                }

            # Extract metadata with proper fallbacks
            title = entry.find("{http://www.w3.org/2005/Atom}title")
            title = title.text.strip() if title is not None else "Unknown Title"

            authors = [
                author.find("{http://www.w3.org/2005/Atom}name").text
                for author in entry.findall("{http://www.w3.org/2005/Atom}author")
                if author.find("{http://www.w3.org/2005/Atom}name") is not None
            ]

            published = entry.find("{http://www.w3.org/2005/Atom}published")
            published = published.text.strip() if published is not None else "0000-00-00T00:00:00Z"

            link = entry.find("{http://www.w3.org/2005/Atom}id")
            link = link.text.strip() if link is not None else ""

            return {
                "title": title,
                "authors": authors,
                "published": published,
                "link": link
            }

        except ET.ParseError as e:
            print(f"Failed to parse XML from ArXiv API for query {arxiv_query}: {e}")
            return {
                "title": "Unknown Title",
                "authors": [],
                "published": "0000-00-00T00:00:00Z",
                "link": ""
            }

        except requests.exceptions.RequestException as e:
            print(f"Network or API error for query {arxiv_query}: {e}, retrying...")
            time.sleep(2 ** attempt)  
            continue

    # If all retries fail
    print(f"Failed to fetch metadata for {arxiv_query} after {retries} attempts.")
    return {
        "title": "Unknown Title",
        "authors": [],
        "published": "0000-00-00T00:00:00Z",
        "link": ""
    }

if __name__ == "__main__":
    # Example queries for testing the function
    test_queries = [
        "id:1706.03762",  
    ]

    for query in test_queries:
        print(f"Fetching metadata for query: {query}")
        metadata = fetch_arxiv_metadata(query)
        print("Metadata retrieved:")
        print(metadata)
        print("-" * 50)  # Separator for readability