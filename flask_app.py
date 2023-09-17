from flask import Flask, send_from_directory, render_template, request
import os

from reference_sentences import retrieve_reference_dicts
from arxiv_num_extraction import get_arxiv_numbers_from_pdf

from arxiv_num_extraction import get_arxiv_numbers_from_pdf
from output_for_app import get_references_from_page

paper_name = 'new.pdf'
arxiv_nums = get_arxiv_numbers_from_pdf(paper_name)
reference_dicts = retrieve_reference_dicts(paper_name)
#r, l = get_references_from_page(reference_dicts, arxiv_nums, page_num=2, type='bm25')
#print(r)
# join the list of set of references into a single list seperated by newline
# new_list = []
# for item in r:
#     joined = ""
#     joined += str(item[0]) + "\n"
#     joined += item[1] + "\n"
#     joined += item[2] + "\n"
#     new_list.append(joined)

# print(new_list)

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('input_form.html')

@app.route('/submit', methods=['POST'])
def submit():
    page = request.form['page']
    page = int(page)
    toggle_status = 'switch' in request.form
    print(toggle_status)
    if toggle_status:
        r, l = get_references_from_page(reference_dicts, arxiv_nums, page_num=page, type='crossencoder')
    else:
        r, l = get_references_from_page(reference_dicts, arxiv_nums, page_num=page, type='bm25')
    new_list = []
    for item in r:
        joined = ""
        joined += str(item[0]) + "\n"
        joined += item[1] + "\n"
        joined += item[2] + "\n"
        new_list.append(joined)

    return render_template('output.html', list1=new_list, list2=l)

if __name__ == '__main__':
    app.run(debug=True, port=9000)
