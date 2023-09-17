from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize
import re


def get_reader(path):
    reader = PdfReader(path)
    return reader

# for adjusting spaces and commas in brackets
def adjust_bracket_spaces(s):
    def replace_comma_spaces(match):
        """Function to replace spaces around commas in the matched string."""
        return re.sub(r'\s*,\s*', ', ', match.group())

    # Remove spaces between brackets and single numbers
    s_modified = re.sub(r'\[\s*(\d+)\s*\]', r'[\1]', s)

    # Correct spaces around commas inside brackets using the helper function
    s_modified = re.sub(r'\[\d+(\s*,\s*\d+)+\]', replace_comma_spaces, s_modified)

    return s_modified


def get_sentences_from_page(page):
    sentences = sent_tokenize(page)
    #remove newlines
    sentences = [s.replace('\n', ' ') for s in sentences]
    sentences = [adjust_bracket_spaces(s) for s in sentences]
    return sentences

# check if there is a reference in sentence (overkill)
def contains_integer_list(s):
    return bool(re.search(r'\[\s*\d+(?:\s*,\s*\d+)+\s*\]', s))


def get_sentences_with_reference(sentences):
    sentences_with_reference = []
    for sentence in sentences:
        if contains_integer_list(sentence):
            sentences_with_reference.append(sentence)
            continue
                 
        elif re.search(r'\[\d+\]', sentence):
            sentences_with_reference.append(sentence)
    return sentences_with_reference

def create_reference_dict(sourced_sentences):
    reference_dict = {}
    for sentence in sourced_sentences:
        #print(sentence)
        # retrieve string between brackets
        reference = re.findall(r'\[(.*?)\]', sentence)
        #print(reference)
        removed_reference = re.sub(r'\[(.*?)\]', '', sentence)
        for r in reference:
            # split by comma
            r = r.split(',')
            # remove spaces
            r = [i.strip() for i in r]
            for i in r:
                if i not in reference_dict:
                    reference_dict[i] = [removed_reference]
                else:
                    reference_dict[i].append(removed_reference)
    return reference_dict

def retrieve_reference_dicts(path):
    reader = get_reader(path)
    reference_dicts = []
    for page in reader.pages:
        page = page.extract_text()
        sentences = get_sentences_from_page(page)
        sourced_sentences = get_sentences_with_reference(sentences)
        reference_dict = create_reference_dict(sourced_sentences)
        reference_dicts.append(reference_dict)
    return reference_dicts


if __name__ == '__main__':
    path = 'attention_paper.pdf'
    item = retrieve_reference_dicts(path)
    print(item)