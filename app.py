from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from analyzer import analyze_content

app = Flask(__name__)

def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        return " ".join([p.get_text() for p in soup.find_all('p')])
    except Exception as e:
        return f"Error fetching URL: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    print("Route / accessed")
    if request.method == "POST":
        print("POST request received")
        content_type = request.form["content_type"]
        print(f"Content type: {content_type}")
        if content_type == "url":
            url = request.form["url"]
            print(f"URL: {url}")
            content = fetch_url_content(url)
            if "Error" in content:
                print(f"URL fetch error: {content}")
                return render_template("index.html", error=content)
        else:
            content = request.form["text"]
            url = None
            print(f"Text content: {content}")
        
        if content:
            print("Analyzing content...")
            result = analyze_content(content, url)
            print(f"Result: {result}")
            return render_template("result.html", result=result, content=content[:100] + "...")
        print("No content retrieved")
        return render_template("index.html", error="No content retrieved.")
    
    print("Rendering index.html for GET")
    return render_template("index.html", error=None)

if __name__ == "__main__":
    app.run(debug=True)