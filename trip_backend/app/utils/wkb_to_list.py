from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape


def wkb_to_list(wkb: WKBElement):
    """Convert WKBElement to Shapely geometry.
    Return list : [latitude, longitude].
    """

    if wkb:
        point = to_shape(wkb)
        return [point.y, point.x]
    return None
