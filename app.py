from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url1 = request.form.get("url1").strip()  # First URL
        url2 = request.form.get("url2").strip()  # Second URL
        element = request.form.get("element")
        results = []

        # Define a function to scrape a single URL
        def scrape_url(url):
            try:
                # Fetch the content of the website
                response = requests.get(url)
                response.raise_for_status()  # Ensure the request was successful

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, "html.parser")

                # Scrape based on the user's selected element
                if element:
                    elements = soup.find_all(element)  # Find all matching elements
                    scraped_content = "\n\n".join([str(elm.prettify()) for elm in elements])
                else:
                    # If no element is provided, scrape the entire HTML
                    scraped_content = soup.prettify()

                return {"url": url, "html_content": scraped_content}
            except requests.exceptions.RequestException as e:
                return {"url": url, "error": str(e)}

        # Scrape both URLs if provided
        if url1:
            results.append(scrape_url(url1))
        if url2:
            results.append(scrape_url(url2))

        return render_template("index.html", results=results, element=element)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
