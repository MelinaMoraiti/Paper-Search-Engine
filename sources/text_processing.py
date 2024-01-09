import nltk
import string
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
def tokenize_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    return tokens
# Sanitizes text from punctuation and stopwords
def clean_tokens(tokens):
    stop_words = set(stopwords.words('english'))
    cleaned_tokens =[]
    for token in tokens:
        if token not in string.punctuation and token not in stop_words:
            cleaned_tokens.append(token)
    return cleaned_tokens
def normalize_tokens(tokens,option):
    if option == 'l':
        lemmatizer = WordNetLemmatizer()
        normalized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    elif option== 's':
        stemmer = PorterStemmer()
        normalized_tokens = [stemmer.stem(token) for token in tokens]
    else:
        raise ValueError("Invalid option. Use 'l' for lemmatization or 's' for stemming.")
    return normalized_tokens
def preprocess_text(text):
    tokens = tokenize_text(text)
    cleaned_tokens = clean_tokens(tokens)
    normalized_tokens = normalize_tokens(cleaned_tokens, option='l')
    cleaned_text = ' '.join(normalized_tokens)
    return cleaned_text
def preprocess_paper(paper):
    text_paper_metadata = f"{paper['Title']} {paper['Authors']} {paper['Abstract']} {paper['Subject_Tags']} {paper['Subjects']} {paper['Submitted Date']}"
    return preprocess_text(text_paper_metadata)

