import requests as rq
from bs4 import BeautifulSoup

def get_html(url):
    """
    Function to get the HTML content of a webpage.
    """
    try:
        response = rq.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except rq.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

data = get_html("https://www.toyota.com/4runner/features/mpg_other_price/8642/8648/8634")
#print(data)
soup = BeautifulSoup(data, "html.parser")
s = soup.find_all("div", class_="tcom-accordion")

for i in s:
    for j in i.children:
        print(j)

print(s)