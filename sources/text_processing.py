# text_processing.py
import nltk
import string,re
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
def tokenize_text(text):
    # Lowercasing
    text = text.lower()
    # Tokenization
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
def preprocess_paper(paper):
    text_content = f"{paper['Title']} {paper['Authors']} {paper['Abstract']} {paper['Subject_Tags']} {paper['Subjects']} {paper['Submitted Date']}"

    # Tokenize the text
    tokens = tokenize_text(text_content)
    
    # Clean the tokens from punctuation and stopwords
    cleaned_tokens = clean_tokens(tokens)

    # Normalize tokens based on the specified option ('l' for lemmatization, 's' for stemming)
    normalized_tokens = normalize_tokens(cleaned_tokens, option='l')
    # Join tokens back into a clean text
    cleaned_text = ' '.join(normalized_tokens)

    return cleaned_text
