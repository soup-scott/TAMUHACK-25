import requests as rq
import re

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
    
def parsevehiclecard(str):
    cardict = {}

    pattern = re.compile(r'data-basemsrp="57625"')
    cardict.update({"Base MSRP": pattern.match(str)})



data = get_html("https://www.toyota.com/all-vehicles/")

soup = BeautifulSoup(data, "html.parser")
s = soup.find_all("div", class_="vehicle-card")

cardicts = []
print(s[3])

for i in s:
    msrp = i.get("data-basemsrp")
    categoy = i.get("data-category")
    citympg = i.get("data-citympg")
    combinedmilage = i.get("data-combinedmpg")
    displayname = i.get("data-display-name")
    hwympg = i.get("data-hwympg")
    imageurl = i.get("data-jelly")
    seating = i.get("data-seating")
    year = i.get("data-year")
    range = i.get("data-range")
    cardict = {
        "Display Name": displayname,
        "MSRP": msrp,
        "Category": categoy,
        "City MPG": citympg,
        "Combined Mileage": combinedmilage,
        "Hwy MPG": hwympg,
        "Image URL": imageurl,
        "Seating": seating,
        "Year": year,
        "Range": range
    }
    cardicts.append(cardict)

if __name__ == "__main__":
    print(cardicts)
    print(len(cardicts))
