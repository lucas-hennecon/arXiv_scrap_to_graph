"""
This file contains functions that retrieve all the arXiv papers corresponding to a given method from the PapersWithCode website
"""

from typing import Set, List, Dict
import requests
import re
from bs4 import BeautifulSoup 
from getReferencesArticles import extract_arxiv_references_from_article
from processPdf import extract_text_from_pdf
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

def retrieve_arxiv_id(paper_url: str) -> str|None:
    """
    Retrieve the arXiv id of a given paper from the PapersWithCode website. Returns None if the paper is not on arXiv.
    :param paper_url: the url of the paper on the PapersWithCode website
    :return: The id of the arXiv paper corresponding to the method
    """
    html = requests.get(f'https://paperswithcode.com{paper_url}')
    arxiv_id = re.findall(r"https:\/\/arxiv\.org\/pdf\/[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*\.pdf", html.text)
    return arxiv_id[0].split("/")[-1].strip(".pdf") if arxiv_id else None

def get_method_id_for_api(method_name: str) -> int|None:
    """
    Retrieve the id of a method from the PapersWithCode API
    :param method_name: the name of the method
    :return: The id of the method
    """
    html = requests.get(f"https://paperswithcode.com/method/{method_name}")
    soup = BeautifulSoup(html.text, 'html.parser')
    
    # Extract the script tag content
    script_tags = soup.find_all('script')
    method_id = None

    for script in script_tags:
        if script.string and "DATATABLE_PAPERS_FILTER_VALUE" in script.string:
            # Extract the method_id using regex
            match = re.search(r"DATATABLE_PAPERS_FILTER_VALUE\s*=\s*'(\d+)'", script.string)
            if match:
                method_id = match.group(1)
                break

    if not method_id:
        print("Method ID not found in the HTML.")
    
    print(f"Extracted Method ID: {method_id}")

    return int(method_id) if method_id else None



def get_paper_urls_from_api_response(method_id: int) -> Set[str]:
    """
    Retrieve the arXiv ids of the papers corresponding to a method from the PapersWithCode API
    :param endpoint_url: the url of the endpoint of the PapersWithCode API
    :return: The list of ids of the arXiv papers corresponding to the method
    """
    endpoint = f"https://paperswithcode.com/api/internal/papers/?format=json&papermethod__method_id={str(method_id)}"

    response = requests.get(endpoint)
    response.raise_for_status()  # Raise an error for HTTP response codes >= 400
    
    data = response.json()
    paper_urls = set()

    print(f"{data['count']} papers found" )
    page_number = 1
    while True: # Loop through all the pages of the API response
        print(f"Page {page_number}")
        for paper in data['results']:
            paper_urls.add(paper['url'])
            
        if data['next'] is None:
            break
        else:
            data = requests.get(data['next']).json()
            page_number += 1

    print('Paper URLs length:', len(paper_urls))
    return paper_urls


def scrape_paper_ids_from_method_page(method_name: str) -> List[str]:
    """
    Scrape the arXiv ids of the papers corresponding to a method from the PapersWithCode website
    :param method_name: the name of the method
    :return: The list of ids of the arXiv papers corresponding to the method
    """
    method_id = get_method_id_for_api(method_name)
    paper_ids: List[str] = []
    if method_id is None:
        print('Unable to get method id required for API call')
        return paper_ids
    paper_urls = get_paper_urls_from_api_response(method_id)
    for url in paper_urls:
        paper_id = retrieve_arxiv_id(url)
        if paper_id:
            paper_ids.append(paper_id)
    return paper_ids
    

# Main function
def compute_method_graph(method_name: str) -> Dict[str, List[str]]:
    """
    Compute the graph of papers corresponding to a method from the PapersWithCode website
    :param method_name: the name of the method
    :return: The graph of papers corresponding to the method. The keys are the ids of the papers and the values 
    are the ids of the papers that the key paper references
    """
    method_id = get_method_id_for_api(method_name)
    if method_id is None:
        print('Unable to get method id required for API call')
        return {}
    paper_urls = get_paper_urls_from_api_response(method_id)
    paper_ids: List[str] = [paper_id for paper_id in (retrieve_arxiv_id(paper) for paper in paper_urls) if paper_id is not None]
    graph: Dict[str, List[str]] = dict.fromkeys(paper_ids, [])

    def process_paper(paper_id: str) -> List[str]:
        text = extract_text_from_pdf(f"http://arxiv.org/pdf/{paper_id}")
        references = extract_arxiv_references_from_article(text)
        return [ref for ref in references if ref in paper_ids]

    # # Parallelize attempt with threads
    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     future_to_paper_id = {executor.submit(process_paper, paper_id): paper_id for paper_id in graph}
    #     for future in tqdm(as_completed(future_to_paper_id), total=len(graph)):
    #         paper_id = future_to_paper_id[future]
    #         try:
    #             graph[paper_id] = future.result()
    #         except Exception as e:
    #             print(f"Error processing paper {paper_id}: {e}")

    # # Parallelize attempt with processes
    # with ProcessPoolExecutor(max_workers=4) as executor:
    #     future_to_paper_id = {executor.submit(process_paper, paper_id): paper_id for paper_id in graph}
    #     for future in tqdm(as_completed(future_to_paper_id), total=len(graph)):
    #         paper_id = future_to_paper_id[future]
    #         try:
    #             graph[paper_id] = future.result()
    #         except Exception as e:
    #             print(f"Error processing paper {paper_id}: {e}")


    for paper_id in tqdm(graph):
        graph[paper_id] = process_paper(paper_id)

    return graph


if __name__ == "__main__":
    # papers_with_code_url = "https://paperswithcode.com/paper/finite-scalar-quantization-vq-vae-made-simple"
    # print(retrieve_arxiv_id(papers_with_code_url))
    # print(get_paper_urls_from_api_response(468))
    # print(get_method_id_for_api("vae"))
    # print(retrieve_arxiv_id('/paper/applying-rlaif-for-code-generation-with-api'))
    # print(scrape_paper_ids_from_method_page("rlaif"))
    print(compute_method_graph('rlaif'))
    # print(extract_arxiv_references_from_article('2408.17072v1'))
