from app.overpass import overpass_camp_site
from app.scrap import scrap_nodes


def mainer():
    if False:
        from app.db import Marker, Tag, TagValues, session
        from sqlalchemy.exc import SQLAlchemyError

        try:
            with session.begin():
                markers = session.query(Marker).all()
                for marker in markers:
                    print(marker.name, marker.location, marker.author_id)
                print("*****TAGS")
                tags = session.query(Tag).all()
                for tag in tags:
                    print(tag.name, tag.display_name)
        except SQLAlchemyError as e:
            print(f"Error: {e}")
        finally:
            session.close()

    xml_data = overpass_camp_site(59, 9, 60, 10)
    nodes = scrap_nodes(xml_data)
    print(f"LEN NODES {len(nodes)}")
    print(nodes)
