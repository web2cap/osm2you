from sqlalchemy.exc import SQLAlchemyError

from .db import Marker, session


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
