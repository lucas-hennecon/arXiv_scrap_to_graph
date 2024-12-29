"""
Helper function to extract the ArXiv references codes from an article 
"""

import re
from typing import List


# TODO: Improve the function to return other references than ArXiv references
def extract_arxiv_references_from_article(text: str) -> List[str]:
    """
    Extracts arXiv references in the formats 'arXiv:2001.08361' and 'abs/2001.08361'.
    
    :param text: The input text containing arXiv references.
    :return: A list of extracted arXiv IDs (e.g., '2001.08361').
    """
    #First version:
    # references = re.findall(r"arXiv:\d{4}\.\d{4,5}", text)
    # references = [reference.split(":")[1] for reference in references]

    # Match both arXiv:XXXX.XXXX and abs/XXXX.XXXX formats
    references = re.findall(r"(?:arXiv:|abs/)(\d{4}\.\d{4,5})", text)


    return references


if __name__ == "__main__":
    from processPdf import extract_text_from_pdf

    text = extract_text_from_pdf("https://arxiv.org/pdf/1706.03762")
    references = extract_arxiv_references_from_article(text)
    print(references, len(references))
