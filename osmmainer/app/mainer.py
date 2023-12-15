from app.db import Marker, session
from app.overpass import overpass_camp_site
from sqlalchemy.exc import SQLAlchemyError


def mainer():
    try:
        with session.begin():
            markers = session.query(Marker).all()
            for marker in markers:
                print(marker.name, marker.location, marker.author_id)
    except SQLAlchemyError as e:
        print(f"Error: {e}")
    finally:
        session.close()

    south = -90
    west = -180
    north = 90
    east = 180

    from bs4 import BeautifulSoup

    # Assuming 'response.text' contains the XML data
    xml_data = overpass_camp_site(south, west, north, east)

    # Parse the XML data with BeautifulSoup
    soup = BeautifulSoup(xml_data, "xml")

    tags = {}

    # Now you can navigate and extract information from the XML structure
    for node in soup.find_all("node"):
        node_id = node.get("id")
        lat = node.get("lat")
        lon = node.get("lon")
        name_tag = node.find("tag", {"k": "name"})
        name = name_tag.get("v") if name_tag else None
        tourism_tag = node.find("tag", {"k": "tourism"})
        tourism = tourism_tag.get("v") if tourism_tag else None
        print(
            f"Node ID: {node_id}, Lat: {lat}, Lon: {lon}, Name: {name}, Tourism: {tourism}"
        )
        for tag in node.find_all("tag"):
            tag_k = tag.get("k")
            if tag_k:
                tags[tag_k] = tags.get(tag_k, 0) + 1
                print(f"\t{tag_k}")

    # tag statistics

    for tag in tags:
        print(f"{tags[tag]}:\t{tag}")
