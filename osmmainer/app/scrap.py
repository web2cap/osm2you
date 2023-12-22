from bs4 import BeautifulSoup


def scrap_nodes(xml_data):
    soup = BeautifulSoup(xml_data, "xml")
    places = []
    for node in soup.find_all("node"):
        place = {}
        place["id"] = node.get("id")
        place["lat"] = node.get("lat")
        place["lon"] = node.get("lon")
        name_tag = node.find("tag", {"k": "name"})
        place["name"] = name_tag.get("v") if name_tag else None
        place["tags"] = {}
        for tag in node.find_all("tag"):
            tag_k, tag_v = tag.get("k"), tag.get("v")
            if tag_k:
                place["tags"][tag_k] = tag_v
        places.append(place)
    return places
