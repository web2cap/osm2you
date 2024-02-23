import logging

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ScrapService:
    @staticmethod
    def scrap_nodes(xml_data):
        """
        Extract information from XML data containing node details.

        Args:
            xml_data (str): XML data containing node details.

        Returns:
            list: A list of dictionaries, each representing a place/node with its attributes.
        """
        try:
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
        except Exception as e:
            logger.error(f"Error occurred while scraping nodes: {e}")
            return None
