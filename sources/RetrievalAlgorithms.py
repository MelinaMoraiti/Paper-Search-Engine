from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
class RetrievalAlgorithms:
    @staticmethod
    def vector_space_model(query, documents,similarity_threshold=0.0):
        # Combine query and documents for vectorization
        all_texts = [query] + list(documents.values())

        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer()

        # Fit and transform the combined text
        tfidf_matrix = vectorizer.fit_transform(all_texts)

        # Separate query vector and document vectors
        query_vector = tfidf_matrix[0]
        document_vectors = {doc_id: tfidf_matrix[i] for i, doc_id in enumerate(documents.keys(), start=1)}

        # Convert sparse matrices to dense arrays for simplicity
        query_vector = np.array(query_vector.todense()).flatten()
        document_vectors = {doc_id: np.array(doc_vector.todense()).flatten() for doc_id, doc_vector in document_vectors.items()}

        # Calculate cosine similarity between the query vector and each document vector
        similarities = {}
        for doc_id, doc_vector in document_vectors.items():
            cosine_similarity_value = cosine_similarity([query_vector], [doc_vector])[0][0]
            similarities[doc_id] = cosine_similarity_value

        # Filter documents based on the similarity threshold
        matching_document_ids = [doc_id for doc_id, similarity in similarities.items() if similarity >= similarity_threshold]

        return matching_document_ids
    #@staticmethod
    #def okapi_bm25(query, documents):