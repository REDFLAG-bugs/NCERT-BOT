import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

class BeautifulSoupScraper:
    @staticmethod
    def extract_text_from_url(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for unwanted in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'form']):
                unwanted.decompose()
            paragraphs = soup.find_all('p')
            text = "\n".join([para.get_text() for para in paragraphs])
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            text = ""
        return text

    @staticmethod
    def filter_text(text):
        unwanted_keywords = ['advertisement', 'subscribe', 'follow us', 'footer', 'comment', 'social', 'share']
        filtered_lines = [line for line in text.split('\n') if not any(keyword in line.lower() for keyword in unwanted_keywords)]
        filtered_text = "\n".join(filtered_lines)

        filtered_text = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', '', filtered_text)
        filtered_text = re.sub(r'\b\d{10,}\b', '', filtered_text)
        filtered_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', filtered_text)
        
        filtered_words = [word for word in filtered_text.split() if word.lower() not in stop_words]
        filtered_text = ' '.join(filtered_words)
        
        return filtered_text

    @staticmethod
    def extract_and_filter_text(links):
        texts = []
        for link in links:
            try:
                text = BeautifulSoupScraper.extract_text_from_url(link)
                filtered_text = BeautifulSoupScraper.filter_text(text)
                texts.append(filtered_text)
            except Exception as e:
                print(f"Failed to extract or filter text from {link}: {e}")
        return texts

