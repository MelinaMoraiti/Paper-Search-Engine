from text_processing import preprocess_text,tokenize_text
class QueryProcessor:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index
    def process_query(self, user_query):
        query_tokens = tokenize_text(user_query) # Only tokenize the user query
        results = self.boolean_retrieval(query_tokens)
        return results
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