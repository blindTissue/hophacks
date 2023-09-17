import requests
import os
import pdfminer
from pdfminer.high_level import extract_text


def download_arxiv_pdfs_from_number(number, save_path='pdf_save'):
    url = "https://arxiv.org/pdf/" + number
    response = requests.get(url)
    save_name = os.path.join(save_path, number + '.pdf')

    # Check if the request was successful
    if response.status_code == 200:
        with open(save_name, 'wb') as file:
            file.write(response.content)
    else:
        print('Request was not successful.')

def clean_paragraphs(s):
    # Split the input into chunks by double newlines
    chunks = s.split('\n\n')
    
    cleaned_paragraphs = []
    
    for chunk in chunks:
        # For each chunk, filter out lines that are too short or standalone characters
        cleaned_lines = [line for line in chunk.split('\n') if len(line.strip()) > 2]
        if cleaned_lines:
            cleaned_paragraphs.append('\n'.join(cleaned_lines))
    
    # Join the cleaned paragraphs with double newlines and return
    return '\n\n'.join(cleaned_paragraphs)


if __name__ == '__main__':
    download_arxiv_pdfs_from_number('2103.00001')

