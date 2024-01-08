import math
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from text_processing import tokenize_text
class OkapiBM25:
    def __init__(self, documents, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.avg_doc_length = 0
        self.doc_lengths = {}
        self.idf = {}
        self.vectorizer = TfidfVectorizer()
        self.documents = documents
        # Initialize the Okapi BM25 model with the provided documents
        for doc_id, text in self.documents.items():
            self.add_document(doc_id, text)

    def add_document(self, doc_id, text):
        # Tokenize the text
        tokens = tokenize_text(text)
        # Calculate document length
        doc_length = len(tokens)
        self.doc_lengths[doc_id] = doc_length
        # Update average document length
        self.avg_doc_length = (self.avg_doc_length * (len(self.doc_lengths) - 1) + doc_length) / len(self.doc_lengths)
        # Update document frequency (DF) and inverse document frequency (IDF) for each term
        term_counts = Counter(tokens)
        for term, count in term_counts.items():
            if term not in self.idf:
                self.idf[term] = 1
            self.idf[term] += 1

    def calculate_bm25_score(self, query, doc_id):
        # Tokenize the query
        query_tokens = tokenize_text(query)
        # Get document length
        doc_length = self.doc_lengths.get(doc_id, 0)
        # Calculate BM25 score
        score = 0
        for term in query_tokens:
            tf = Counter(self.vectorizer.build_analyzer()(self.documents[doc_id]))[term]
            idf = math.log((len(self.doc_lengths) - self.idf.get(term, 0) + 0.5) / (self.idf.get(term, 0) + 0.5) + 1)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
            score += idf * numerator / denominator
        return score
    def retrieve(self, query,score_threshold=1.0):
        scores = [(doc_id, self.calculate_bm25_score(query, doc_id)) for doc_id in self.documents]
        # Filter documents based on the score threshold
        matching_documents = [doc_id for doc_id, score in scores if score >= score_threshold]
        # Sort documents by score in descending order
        ranked_documents = sorted(matching_documents, key=lambda x: x[1], reverse=True)
        return ranked_documents

