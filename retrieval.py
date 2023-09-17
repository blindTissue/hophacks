from sentence_transformers import CrossEncoder
from rank_bm25 import BM25Okapi

def crossencoder_response(corpus, query):
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    cross_inp = [[query, sent] for sent in corpus]
    cross_scores = cross_encoder.predict(cross_inp)
    scores_and_sents = list(zip(cross_scores, corpus))
    scores_and_sents.sort(reverse=True)
    return scores_and_sents[0][1]


def bm25_search(corpus, query):
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    query = query.lower()
    tokenized_query = query.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    # get the index of the highest score

    ranked_docs = [corpus[i] for i in sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)]
    return ranked_docs[0]