import PyPDF2
import os

def get_text(path):
    reader = PyPDF2.PdfReader(path)
    text=""
    for page in reader.pages:
        text += page.extract_text().lower()
    text = text.split("references")[0]
    return text

def max_line_length(text):
    max_length = 0
    for line in text.split("\n"):
        if len(line) > max_length:
            max_length = len(line)
    return max_length

def soft_max_line_length(text):
    length_list = []
    for line in text.split("\n"):
        length_list.append(len(line))
    length_list.sort()
    return length_list[int(len(length_list) * 0.9)]

def create_paragraph_list(text, max_len):
    paragraph_list = []
    paragraph = ""
    for line in text.split("\n"):
        if len(line) < max_len / 2:
            if paragraph != "":
                paragraph += line.lower()
                paragraph = paragraph.replace("  ", " ")
                paragraph_list.append(paragraph)
            paragraph = ""
        else:
            paragraph += line.lower() + " "
    return paragraph_list

def get_paragraphs(path):
    text = get_text(path)
    #max_len = max_line_length(text)
    max_len = soft_max_line_length(text)
    paragraph_list = create_paragraph_list(text, max_len)
    paragraph_list = [paragraph.strip().replace("  ", " ") for paragraph in paragraph_list if len(paragraph) > 0]
    return paragraph_list

