import logging

from django.core.management import call_command
from django.db import transaction

from core.managers.nodes_to_markers_updater import NodesToMarkersUpdaterManager
from core.services.markers import MarkerService
from core.services.overpass import OverpassService
from core.services.related_markes_scrap import RelatedMarkerScrapService
from core.services.scrape import ScrapService
from core.tasks import run_scrap_markers_batch_related

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
        result = NodesToMarkersUpdaterManager.update_markers(nodes, True)
        call_command("clustermarkers")
        run_scrap_markers_batch_related.delay()
        return result

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
            markers_by_squares = RelatedMarkerScrapService.get_all_squares_by_pack()
            results = []
            for marker_square in markers_by_squares:
                for markers in markers_by_squares[marker_square]:
                    with transaction.atomic():
                        logger.warning(f"Starting overpass batch {marker_square}")
                        xml_data = overpass_service.overpass_batch_related_nodes(
                            markers
                        )
                        nodes = ScrapService.scrap_nodes(xml_data)
                        result = str(NodesToMarkersUpdaterManager.update_markers(nodes))
                        RelatedMarkerScrapService.delete_pack(markers)
                        logger.warning(f"Addad related batch {marker_square}: {result}")
                        results.append(marker_square)
            return "\n".join(results)
        except Exception as e:
            logger.exception(f"Error occurred while handle_related_batch_scenario: {e}")
