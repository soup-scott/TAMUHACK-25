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

def generate_color_dict(url):
    data_color = get_html(url)
    #print(data)
    soup_color = BeautifulSoup(data_color, "html.parser")
    s_color = soup_color.find_all("button", class_="color-selector__swatch")

    color_dict = {}

    for color in s_color:
        label = color.get("aria-label")
        hex = color.get("data-color-hex")

        labellist = label.split(" ")
        if labellist[-1][0] == "[":
            extra_color_cost = True
            label = ""
            for j in range(len(labellist)-1):
                label += labellist[j] + " "
        else:
            extra_color_cost = False
        color_dict[label] = {
            "hex": hex,
            "extra_color_cost": extra_color_cost
        }
    return color_dict





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
    data_range = i.get("data-range")
    aa_name = i.get("data-aa-series-code")
    car_string = "https://www.toyota.com/"+aa_name+"/"#section/features/"
    print(car_string)


    try:
        color_dict = generate_color_dict(car_string)
    except:
        print("COLOR ERROR AHHHHH")
        print(displayname)
        print(aa_name)
        color_dict = {"white": {"hex": "#FFFFFF", "extra_color_cost": False}}
    
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
        "Range": data_range,
        "Colors": color_dict
    }
    cardicts[displayname] = cardict

json_string = json.dumps(cardicts, indent=4)
f = open("test.json", "w")
f.write(json_string)
f.close()
'''
if __name__ == "__main__":
    print(json_string)
    print("\n\n\n\n")
    print(cardicts)
    print(len(cardicts))
'''
