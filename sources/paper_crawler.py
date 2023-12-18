import requests
from bs4 import BeautifulSoup

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
    
def create_urls(search_queries,max_results_per_page, total_results,search_type='all',order=''):
    target_urls=[]
    base_url = 'https://arxiv.org/search/?'
    for search_query in search_queries:
        total_pages = (total_results + max_results_per_page - 1) // max_results_per_page
        for page in range(total_pages):
            start = page * max_results_per_page
            query = f'query={search_query}&searchtype={search_type}&abstracts=show&order={order}&size={max_results_per_page}&start={start}'
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
        # Subject Tags
        subject_codes = ', '.join([tag.text.strip() for tag in paper.find_all('span', class_=lambda value: value and value.startswith('tag is-small'))])
        subjects = ', '.join([tag['data-tooltip'] for tag in paper.find_all('span', class_=lambda value: value and value.startswith('tag is-small'))])

        title = paper.find('p', class_='title').text.strip()
        # Authors
        authors_p = paper.find('p', class_='authors')
        if authors_p:
            authors =', '.join([author.text.strip() for author in authors_p.find_all('a')])
        # Submission Date
        dates = paper.find('p',class_='is-size-7')
        submitted_span = dates.find('span', class_='has-text-black-bis has-text-weight-semibold')
        submitted_date = submitted_span.next_sibling.strip()
        # Abstract
        abstract_span = paper.find('span', class_='abstract-full')
        a_element = abstract_span.find('a').decompose()
        abstract = abstract_span.text.strip()
        # Add data to the list
        if abstract:
            paper_list.append({
                'arXiv ID': arxiv_id,
                'PDF Link': pdf_link,
                'Subject_Tags': subject_codes,
                'Subjects': subjects,
                'Title': title,
                'Authors': authors,
                'Abstract': abstract,
                'Submitted Date': submitted_date
            })
    return paper_list

