from text_processing import preprocess_text,tokenize_text
from VectorSpaceModel import VectorSpaceModel
from OkapiBM25 import OkapiBM25
class QueryProcessor:
    def __init__(self, inverted_index,preprocessed_docs):
        self.inverted_index = inverted_index
        self.vector_space_model = VectorSpaceModel(preprocessed_docs)
        self.okapi_bm25 = OkapiBM25(preprocessed_docs)
    def process_query(self, user_query):
        query_tokens = tokenize_text(preprocess_text(user_query)) 
        vsm_results = self.vector_space_model.retrieve(preprocess_text(user_query),0.05)
        bm25_results = self.okapi_bm25.retrieve(preprocess_text(user_query),3.0)
        boolean_results = self.boolean_retrieval(query_tokens)
        return boolean_results,vsm_results,bm25_results
    def boolean_retrieval(self,processed_query_tokens):
        current_documents = None # initialize current docs with None
        current_operator = 'AND'  # Default to AND
        for token in processed_query_tokens:
            if token.upper() in {'AND', 'OR', 'NOT'}:
                # Update the current operator
                current_operator = token.upper()
            else:
                term_documents = set(self.inverted_index.index.get(token, {}).keys())
                 # Update the set of current documents based on the current operator
                if current_operator == 'AND':
                     # If this is the first term, set current_documents to the term_documents
                    if current_documents is None:
                        current_documents = term_documents
                    else:
                        current_documents = current_documents.intersection(term_documents)
                    current_documents = current_documents.intersection(term_documents)
                elif current_operator == 'OR':
                    current_documents = current_documents.union(term_documents)
                elif current_operator == 'NOT':
                    current_documents = current_documents.difference(term_documents)
        result_documents = current_documents 
        return result_documents