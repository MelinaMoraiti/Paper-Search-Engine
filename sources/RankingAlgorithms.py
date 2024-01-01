from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class RankingAlgorithm:
    @staticmethod
    def tf_idf_ranking(documents, query):
        # Combine query and document texts
        all_texts = [query] + list(documents.values())
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        # Fit and transform the combined text
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        # Separate query vector and document vectors
        query_vector = tfidf_matrix[0]
        document_vectors = tfidf_matrix[1:]
        # Convert sparse matrices to dense arrays for simplicity
        query_vector = np.array(query_vector.todense()).flatten()
        document_vectors = [np.array(doc_vector.todense()).flatten() for doc_vector in document_vectors]
        # Calculate cosine similarity between the query vector and each document vector
        similarities = [np.dot(query_vector, doc_vector) for doc_vector in document_vectors]
        # Sort documents by similarity in descending order
        sorted_documents = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
        # Return document IDs in sorted order
        ranked_document_ids = [list(documents.keys())[index] for index, _ in sorted_documents]

        return ranked_document_ids

