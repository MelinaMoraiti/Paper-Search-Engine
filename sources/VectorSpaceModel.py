from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorSpaceModel:
    def __init__(self,documents):
        self.documents = documents
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
    def add_document(self, doc_id, text):
        self.documents[doc_id] = text
    def build_tfidf_matrix(self):
        all_texts = list(self.documents.values())
        self.tfidf_matrix = self.vectorizer.fit_transform(all_texts)
    def calculate_similarity(self, query):
        if self.tfidf_matrix is None:
            self.build_tfidf_matrix()
        query_vector = self.vectorizer.transform([query])
        document_vectors = self.tfidf_matrix
        similarities = cosine_similarity(query_vector, document_vectors).flatten()
        return similarities
    def retrieve(self, query,similarity_threshold=0.5):
        similarities = self.calculate_similarity(query)
        # Retrieve document IDs with similarity above the threshold
        matching_document_ids = [doc_id for doc_id, similarity in zip(self.documents.keys(), similarities) if similarity >= similarity_threshold]
        return matching_document_ids
    def tf_idf_ranking(self, query):
        similarities = self.calculate_similarity(query)
        # Sort documents by similarity in descending order
        sorted_documents = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
        # Return document IDs in sorted order
        ranked_document_ids = [list(self.documents.keys())[index] for index, _ in sorted_documents]
        return ranked_document_ids


