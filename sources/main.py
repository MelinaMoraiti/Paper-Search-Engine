import paper_crawler
import file_operations
from text_processing import preprocess_paper
from InvertedIndex import InvertedIndex
from QueryProcessor import QueryProcessor
'''
categories = ['cs','cond-mat','astro-ph','math','q-bio','q-fin','gr-qc','hep-ex','hep-lat','hep-ph','hep-th','math-ph','nlin','nucl-ex','nucl-th','physics','quant-ph','stat','econ']  
#query = ['Distributed Systems']

target_urls = paper_crawler.create_urls(categories,200,1000)
papers_data = paper_crawler.crawl_websites(target_urls)
# Saving Data in files.
file_operations.save_data(papers_data,'/files/arXiv_papers.json')
file_operations.save_data(papers_data,'/files/arXiv_papers.csv')
'''

# load data from file
papers_collection = file_operations.retrieve_data('../files/arXiv_papers.json')
# text_processing
preprocessed_texts = {}
for paper in papers_collection:
    document_id = paper['arXiv ID']
    preprocessed_texts[document_id] = preprocess_paper(paper)

#Create inverted index
inverted_index = InvertedIndex()
# Add papers to the inverted index
for doc_id, preprocessed_text in preprocessed_texts.items():
    inverted_index.add_document(doc_id, preprocessed_text)
terms=["cs.IT"]
inverted_index.print(terms)

user_query = "cs.IT"
query_processor = QueryProcessor(inverted_index)
result_docs = query_processor.process_query(user_query)
print("Matching Documents:", result_docs)


