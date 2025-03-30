import requests
from bs4 import BeautifulSoup
from analyzer import analyze_content

def get_input():
    choice = input("Enter 1 for URL, 2 for text: ")
    if choice == "1":
        url = input("Enter URL: ")
        return fetch_url_content(url)
    else:
        return input("Enter text: ")

def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        return " ".join([p.get_text() for p in soup.find_all('p')])
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None

if __name__ == "__main__":
    content = get_input()
    if content:
        print(f"Content retrieved: {content[:100]}...")
        url = input("Enter URL (or press Enter if no URL): ") or None
        result = analyze_content(content, url)
        print(f"\nVerdict: {result['verdict']} (Confidence: {result['confidence']}%)")
        print("Details:")
        for key, value in result['details'].items():
            print(f"{key}: {value}")