import file_operations
from text_processing import tokenize_text,preprocess_paper
from collections import defaultdict
class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)
    def add_document(self, doc_id, tokens):
        for token in tokens:
            self.index[token].add(doc_id)
    def search(self, query_tokens):
        # Retrieve document IDs for each query token
        result = set.union(*(self.index.get(token, set()) for token in query_tokens))
        return result

papers_collection=file_operations.retrieve_data('arXiv_papers.json')
preprocessed_texts = {}
for paper in papers_collection:
    document_id = paper['arXiv ID']
    preprocessed_texts[document_id] = preprocess_paper(paper)

paper_index = InvertedIndex()
for doc_id, preprocessed_text in preprocessed_texts.items():
    # Tokenize the preprocessed text
    tokens = tokenize_text(preprocessed_text)
    # Add the document to the inverted index
    paper_index.add_document(doc_id, tokens)
# Search for papers containing "transformers" and "language modeling"
query_terms = [""]
result = paper_index.search(query_terms)

print("Papers containing 'bugs':", result)