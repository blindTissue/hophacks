from pdfminer.high_level import extract_text
import re

def extract_references_from_pdf(pdf_path):
    # Extract text from the PDF
    text = extract_text(pdf_path)
    text = text.lower()

    # Find the references section (this can be adjusted based on common patterns)
    references_start = re.search(r'\b(references|bibliography|Works Cited)\b', text)
    
    if not references_start:
        print("References section not found.")
        return

    # Extract the references section (assuming the rest of the document after 'References' is the references section)
    references_text = text[references_start.start():]

    # Split references into individual entries (this is a basic split on numbers. You may need to adjust this regex)
    references = re.split(r'\n(?=\[?\d+\]?\.?)', references_text)

    return references[1:]  # the first item is the "References" title

def get_references_only(references):
    references_only = []
    for reference in references:
        if '[' in reference:
            item = reference.split('[')[1]
            item = '[' + item
            references_only.append(item)
    return references_only

#get item that looks like ****.****
def get_arxiv_number(reference):
    # Extract the arXiv number
    arxiv_number = re.search(r'arxiv:\d{4}\.\d{4,5}(v\d+)?', reference)
    # get rid of arxiv: in the string
    if arxiv_number:
        arxiv_number = arxiv_number.group(0)[6:]
        return arxiv_number
    ref_number = re.search(r'abs/\d{4}\.\d{4,5}(v\d+)?', reference)
    if ref_number:
        ref_number = ref_number.group(0)[4:]
        return ref_number
    return None

def get_arxiv_numbers_from_pdf(pdf_path):
    references = extract_references_from_pdf(pdf_path)
    references_only = get_references_only(references)
    arxiv_numbers = [get_arxiv_number(reference) for reference in references_only]
    return arxiv_numbers


if __name__ == '__main__':
    a = get_arxiv_numbers_from_pdf('attention_paper.pdf')
    print(a)