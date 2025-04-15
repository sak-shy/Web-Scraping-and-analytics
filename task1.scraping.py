import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = "https://tinyurl.com/yfxm6tsm" 
def extract_building_details(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    building_div = soup.find('div', id='DivBuilding')

    if not building_div:
        print("No building details found.")
        return []

    rows = building_div.find_all('tr')
    data = []

    for row in rows[1:]:
        cols = [col.get_text(strip=True) for col in row.find_all('td')]
        if cols:
            data.append(cols)

    return data

 
building_data = extract_building_details(url)


if building_data:
    df = pd.DataFrame(building_data)
    df.to_csv("building_details.csv", index=False)
    print("Saved building details to building_details.csv")
else:
    print(" No data available.")