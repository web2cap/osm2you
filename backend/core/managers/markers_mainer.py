import logging

from django.db import transaction

from core.managers.nodes_to_markers_updater import NodesToMarkersUpdaterManager
from core.services.markers import MarkerService
from core.services.overpass import OverpassService
from core.services.related_markes_scrap import RelatedMarkerScrapService
from core.services.scrape import ScrapService

logger = logging.getLogger(__name__)
overpass_service = OverpassService()


class MarkerMainerCommandManager:
    @staticmethod
    def handle_command(scenario, marker_id=None):
        try:
            if scenario == "main":
                return MarkerMainerScenarioManager.handle_main_scenario()
            elif scenario == "related":
                if marker_id:
                    return (
                        MarkerMainerScenarioManager.handle_related_one_marker_scenario(
                            marker_id
                        )
                    )
                return MarkerMainerScenarioManager.handle_related_batch_scenario()
            else:
                raise ValueError("Invalid scenario. Choose 'main' or 'related'.")
        except Exception as e:
            logger.exception(f"Command execution error: {e}")
            raise


class MarkerMainerScenarioManager:
    @staticmethod
    def handle_main_scenario():
        xml_data = overpass_service.overpass_main_kind_nodes()
        nodes = ScrapService.scrap_nodes(xml_data)
        return NodesToMarkersUpdaterManager.update_markers(nodes)

    @staticmethod
    def handle_related_one_marker_scenario(marker_id):
        marker = MarkerService.get_by_id(marker_id)
        if not marker:
            raise ValueError(f"Error getting marker with id={marker_id}")
        xml_data = overpass_service.overpass_related_nodes(marker.location)
        nodes = ScrapService.scrap_nodes(xml_data)
        return NodesToMarkersUpdaterManager.update_markers(nodes)

    @staticmethod
    def handle_related_batch_scenario():
        try:
            with transaction.atomic():
                markers_by_squares = RelatedMarkerScrapService.get_all_squares_by_pack()
                result = []
                for markers_packages in markers_by_squares.values():
                    for markers in markers_packages:
                        xml_data = overpass_service.overpass_batch_related_nodes(
                            markers
                        )
                        nodes = ScrapService.scrap_nodes(xml_data)
                        result.append(
                            str(NodesToMarkersUpdaterManager.update_markers(nodes))
                        )
                RelatedMarkerScrapService.delete_all()
            return "\n".join(result)
        except Exception as e:
            logger.exception(f"Error occurred while handle_related_batch_scenario: {e}")
