from text_processing import preprocess_text,tokenize_text
class QueryProcessor:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index
    def process_query(self, user_query):
        processed_query = preprocess_text(user_query)
        processed_query_tokens = tokenize_text(user_query)
        results = self.boolean_operations(processed_query_tokens)
        return results
    def boolean_operations(self, processed_query_tokens):
        result_documents = set(self.inverted_index.index.keys())
        for token in processed_query_tokens:
            result_documents = set.intersection(set(self.inverted_index.index[token]))
        return result_documents