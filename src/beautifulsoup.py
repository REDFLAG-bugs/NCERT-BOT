import sys
import os
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from selenium_extracts.selenium import GoogleSearch

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove unwanted sections before extracting text
    for unwanted in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'form']):
        unwanted.decompose()
    
    # Extract text content
    paragraphs = soup.find_all('p')
    text = "\n".join([para.get_text() for para in paragraphs])
    return text

def filter_text(text):
    unwanted_keywords = ['advertisement', 'subscribe', 'follow us', 'footer', 'comment', 'social', 'share']
    filtered_lines = [line for line in text.split('\n') if not any(keyword in line.lower() for keyword in unwanted_keywords)]
    filtered_text = "\n".join(filtered_lines)

    filtered_text = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', '', filtered_text)  # Dates like 12/25/2022
    filtered_text = re.sub(r'\b\d{10,}\b', '', filtered_text)  # Long numbers (phone numbers)
    filtered_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', filtered_text)  # Email addresses
    
    filtered_words = [word for word in filtered_text.split() if word.lower() not in stop_words]
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text

def extract_and_filter_text(links):
    texts = []
    for link in links:
        try:
            text = extract_text_from_url(link)
            filtered_text = filter_text(text)
            texts.append(filtered_text)
        except Exception as e:
            print(f"Failed to extract or filter text from {link}: {e}")
    return texts

if __name__ == '__main__':
    keyword = input("Enter the keyword to search: ")
    try:
        google_search = GoogleSearch()
        google_links = google_search.search(keyword)
        print("Google Search Results:")
        for link in google_links:
            print(link)
        texts = extract_and_filter_text(google_links)
        for i, text in enumerate(texts):
            print(f"Text from {google_links[i]}:")
            print(text)
            print("\n" + "="*80 + "\n")
    except Exception as e:
        print(f"An error occurred during the search process: {e}")

