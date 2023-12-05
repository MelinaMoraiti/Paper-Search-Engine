import requests
from bs4 import BeautifulSoup
import json
import csv

def get_html(url): 
    try: 
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else :
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return ''     
    except Exception as e: 
         print(e) 
         return ''
    
def create_urls(search_queries,max_results,start=0,search_type='all',order=''):
    target_urls=[]
    base_url = 'https://arxiv.org/search/?'
    for search_query in search_queries:
        query = f'query={search_query}&searchtype={search_type}&abstracts=show&order={order}&size={max_results}&start={start}'
        target_url = base_url + query
        target_urls.append(target_url)
    return target_urls

def crawl_websites(urls):
    all_papers = []
    for url in urls:    
        html_content = get_html(url)
        if html_content != '':
            soup = BeautifulSoup(html_content, 'html.parser')
            papers_on_page = soup.find_all('li',class_='arxiv-result')
            if papers_on_page:
                papers_metadata = extract_papers_metadata(papers_on_page)
                all_papers.extend(papers_metadata)
        else:
            return None
    return all_papers
 # Extract metadata (title, authors, abstract, etc.) for each paper in a category 
def extract_papers_metadata(papers): 
    paper_list = []
    for paper in papers:
        links = paper.find('p',class_='list-title is-inline-block')
        arxiv_id = links.find('a', href=True).text.strip()
        pdf_a_tag = links.find('span').find('a')
        if pdf_a_tag:
            pdf_link = pdf_a_tag.get('href') 
        tags = [tag.text.strip() for tag in paper.find_all('span', class_='tag')]
        title = paper.find('p', class_='title').text.strip()
        authors_p = paper.find('p', class_='authors')
        if authors_p:
            authors =', '.join([author.text.strip() for author in authors_p.find_all('a')])
        submitted_date = paper.find('span', string='Submitted').find_next('span').text.strip()
        abstract_span_without_a = paper.find('span', class_='abstract-full').find('a').decompose()
        abstract = abstract_span_without_a.text.strip()
        # Add data to the list
        if abstract:
            paper_list.append({
                'arXiv ID': arxiv_id,
                'PDF Link': pdf_link,
                'Tags': tags,
                'Title': title,
                'Authors': authors,
                'Tags': tags,
                'Abstract': abstract,
                'Submitted Date': submitted_date
            })
    return paper_list

