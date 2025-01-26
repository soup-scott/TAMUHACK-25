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

data = get_html("https://www.toyota.com/4runner/")
soup = BeautifulSoup(data, "html.parser")
s = soup.find_all("h1", class_="title")
for i in s:
    title = i.string
    print(title)
print(s)
print(s[0])