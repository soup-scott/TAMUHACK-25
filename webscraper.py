import requests as rq
from bs4 import BeautifulSoup
import json


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



data = get_html("https://www.toyota.com/all-vehicles/")

soup = BeautifulSoup(data, "html.parser")
s = soup.find_all("div", class_="vehicle-card")

cardicts = {}
json_string = ""

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
    cardicts[displayname] = cardict

json_string = json.dumps(cardicts, indent=4)
f = open("test.json", "w")
f.write(json_string)
f.close()

if __name__ == "__main__":
    print(json_string)
    print("\n\n\n\n")
    print(cardicts)
    print(len(cardicts))
