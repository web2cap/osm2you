from django.conf import settings

CLUSTERING = getattr(settings, "CLUSTERING", {})
CLUSTERING_DENCITY = getattr(settings, "CLUSTERING_DENCITY", 36)


class BboxSquare:

    def __init__(self, in_bbox=None):
        self._bbox_area = self._get_bbox_area(in_bbox)
        self._calculated_square_size = self._calculate_square_size()

    def _get_bbox_area(self, in_bbox):
        """Calculate and return the area of the bounding box specified in the request parameters.

        Returns:
            float: The area of the bounding box.
        """

        if not in_bbox:
            return 360 * 180

        min_lon, min_lat, max_lon, max_lat = map(float, in_bbox.split(","))
        dif_lon = max_lon - min_lon
        if dif_lon > 360:
            dif_lon = 360
        dif_lat = max_lat - min_lat
        if dif_lat > 180:
            dif_lon = 180
        return dif_lon * dif_lat

    def _calculate_square_size(self):
        if self._bbox_area < CLUSTERING["square_size"][0] ** 2 * CLUSTERING_DENCITY:
            return False

        for i in range(1, len(CLUSTERING["square_size"])):
            if self._bbox_area < CLUSTERING["square_size"][i] ** 2 * CLUSTERING_DENCITY:
                return CLUSTERING["square_size"][i - 1]

        return CLUSTERING["square_size"][len(CLUSTERING["square_size"]) - 1]

    def get_square_size(self):
        """Returns the calculated square_size level based on CLUSTERING_DENCITY and bounding box area.

        Returns:
            int or False: The calculated square_size level, or False if the zoom is too large.
        """

        return self._calculated_square_size

    def get_show_clusters(self):
        if self._calculated_square_size:
            return True
        return False
