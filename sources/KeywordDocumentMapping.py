from collections import defaultdict
class KeywordDocumentMapping:
    def __init__(self):
        self.mapping = defaultdict(set)

    def add_mapping(self, keyword, doc_id):
        self.mapping[keyword].add(doc_id)

    def get_documents_for_keyword(self, keyword):
        return self.mapping.get(keyword, set())