from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorSpaceModel:
    def __init__(self,documents):
        self.documents = documents
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.doc_ids = list(self.documents.keys())
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
        sorted_results = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True) #Sort results by similarities
        matching_document_ids = [self.doc_ids[i] for i, similarity in sorted_results if similarity >= similarity_threshold]
        return matching_document_ids