from reference_sentences import retrieve_reference_dicts
from arxiv_num_extraction import get_arxiv_numbers_from_pdf
from retrieval import crossencoder_response, bm25_search
from paragraph import get_paragraphs
import os

from arxiv_num_extraction import get_arxiv_numbers_from_pdf
from output_for_app import get_references_from_page
from utils import download_arxiv_pdfs_from_number

arxiv_nums = get_arxiv_numbers_from_pdf('new.pdf')
# for num in arxiv_nums:
#     if num is not None:
#         download_arxiv_pdfs_from_number(num)

reference_dicts = retrieve_reference_dicts('new.pdf')

r, l = get_references_from_page(reference_dicts, arxiv_nums, page_num=4, type='bm25')
for i in r:
    print(i)