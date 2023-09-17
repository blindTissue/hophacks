from reference_sentences import retrieve_reference_dicts
from arxiv_num_extraction import get_arxiv_numbers_from_pdf
from retrieval import crossencoder_response, bm25_search
from paragraph import get_paragraphs
import os

def create_arxiv_num_sentence_dict(reference_dicts, arxiv_nums, page_num):
    reference_dict = reference_dicts[page_num]
    key_nums = list(reference_dict.keys())
    new_dict = {}
    unfound_nums = []
    for key_num in key_nums:
        int_key = int(key_num) - 1
        arxiv_num = arxiv_nums[int_key]
        if arxiv_num is None:
            unfound_nums.append(key_num)
        else:
            new_dict[arxiv_num] = reference_dict[key_num]
    return new_dict, unfound_nums

def find_similarity(arxiv_dict, arxiv_nums, type='bm25'):
    out = []
    for key in arxiv_dict.keys():
        article_path = os.path.join('pdf_save', key + '.pdf')
        corpus = get_paragraphs(article_path)
        if key == "9":
            print(corpus)
        for sentence in arxiv_dict[key]:
            if type == 'bm25':
                closest = bm25_search(corpus, sentence)
            else:
                closest = crossencoder_response(corpus, sentence)
            arxiv_num = arxiv_nums.index(key)
            out.append((arxiv_num + 1, sentence, closest))

    return out

def get_references_from_page(reference_dicts, arxiv_nums, page_num=1, type='bm25'):
    arxiv_dict, unfound_nums = create_arxiv_num_sentence_dict(reference_dicts, arxiv_nums, page_num)
    out = find_similarity(arxiv_dict, arxiv_nums, type=type)
    return out, unfound_nums