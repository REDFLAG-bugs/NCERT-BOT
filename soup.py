from selenium_extracts.collection import GoogleSearch, YoutubeSearch
import requests
from bs4 import BeautifulSoup




def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    paragraphs = soup.find_all('p')
    text = "\n".join([para.get_text() for para in paragraphs])
    return text


if __name__ == '__main__':
    google_links = GoogleSearch.search('chapter 11 hornbill photograph summary')
    print("Google Search Results:")
    for link in google_links:
        print(link)
    for link in google_links:
        text = extract_text_from_url(link)
        print(f"Text from {link}:")
        print(text)
        print("\n" + "="*80 + "\n")
    