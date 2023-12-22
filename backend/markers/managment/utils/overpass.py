import requests
from django.conf.settings import OVERPASS


def overpass_camp_site(south=-90, west=-180, north=90, east=180):
    params = {
        "data": OVERPASS["camp_site"].format(
            south=south, west=west, north=north, east=east
        )
    }
    response = requests.get(OVERPASS["url"], params=params)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}")
        return None
