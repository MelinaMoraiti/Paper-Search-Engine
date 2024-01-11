from text_processing import tokenize_text
from collections import defaultdict

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(dict)
    def add_document(self, doc_id, preprocessed_text):
        # Tokenize the preprocessed text
        tokens = tokenize_text(preprocessed_text)
        term_freq = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1
        # Update the inverted index only for terms with occurrences
        for term, frequency in term_freq.items():
            if doc_id not in self.index[term]:
                self.index[term][doc_id] = {'frequency': frequency, 'positions': []}
            else:
                self.index[term][doc_id]['frequency'] += frequency
            # Optionally, store positions where the term appears in the document
            positions = [i for i, t in enumerate(tokens) if t == term]
            self.index[term][doc_id]['positions'].extend(positions)
    def get_term_info(self, term):
        return self.index.get(term, {})
    '''
    def print(self, terms):
        for term in terms:
            term_info = self.get_term_info(term)
            sorted_docs = sorted(term_info.items(), key=lambda x: x[1]['frequency'],reverse=True)
            print(f"Inverted Index for term '{term}':")
            for doc_id, doc_info in sorted_docs:
                frequency = doc_info.get('frequency', 0)
                positions = doc_info.get('positions', [])
                print(f"Document ID: {doc_id}, Frequency: {frequency}, Positions: {positions}")
            print("="*50)
    '''



