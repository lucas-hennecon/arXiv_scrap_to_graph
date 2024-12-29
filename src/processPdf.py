import requests
import pdfplumber
import io


def extract_text_from_pdf(url: str) -> str:
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to download the PDF: {response.status_code}")

    pdf_buffer = io.BytesIO(response.content)

    # Extract text from the PDF
    with pdfplumber.open(pdf_buffer) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"

    return all_text


if __name__ == "__main__":
    url = "https://arxiv.org/pdf/1706.03762"
    text = extract_text_from_pdf(url)
    print(text[:1000])  # Print the first 1000 characters of the extracted text
