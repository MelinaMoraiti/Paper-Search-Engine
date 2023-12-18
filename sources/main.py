import paper_crawler
import file_operations
import text_processing
import re

#categories = ['cs','cond-mat','astro-ph','math','q-bio','q-fin','gr-qc','hep-ex','hep-lat','hep-ph','hep-th','math-ph','nlin','nucl-ex','nucl-th','physics','quant-ph','stat','econ']  
#query = ['Distributed Systems']

#target_urls = paper_crawler.create_urls(categories,100,100)
#papers_data = paper_crawler.crawl_websites(target_urls)
# Saving Data in files.
#file_operations.save_data(papers_data,'arXiv_papers.json')
#file_operations.save_data(papers_data,'arXiv_papers.csv')

# load data from file
papers_data=file_operations.retrieve_data('arXiv_papers.json')

print(text_processing.preprocess_paper(papers_data[1350]))
    
#print(text_processing.tokenize_text(papers_data[0]['Title']))
#print(papers_data[2]['Tags'])
#print(text_processing.preprocess_text(papers_data[40]['Subjects'],'s'))
#print(text_processing.preprocess_text(papers_data[0]['Submitted Date'],'l'))
#print(text_processing.normalize_text(papers_data[24]['Abstract']))

