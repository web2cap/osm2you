import logging

from core.managers.nodes_to_markers_updater import NodesToMarkersUpdaterManager
from core.services.markers import MarkerService
from core.services.overpass import OverpassService
from core.services.scrape import ScrapService

logger = logging.getLogger(__name__)


class MarkerMainerCommandManager:
    @staticmethod
    def handle_command(scenario, marker_id=None):
        try:
            if scenario == "main":
                return MarkerMainerScenarioManager.handle_main_scenario()
            elif scenario == "related":
                if not marker_id:
                    raise ValueError(
                        "Main marker id is required for 'related' scenario."
                    )
                return MarkerMainerScenarioManager.handle_related_scenario(marker_id)
            else:
                raise ValueError("Invalid scenario. Choose 'main' or 'related'.")
        except Exception as e:
            logger.exception(f"Command execution error: {e}")
            raise


class MarkerMainerScenarioManager:
    @staticmethod
    def handle_main_scenario():
        xml_data = OverpassService.overpass_main_kind_nodes()
        nodes = ScrapService.scrap_nodes(xml_data)
        return NodesToMarkersUpdaterManager.update_markers(nodes)

    @staticmethod
    def handle_related_scenario(marker_id):
        marker = MarkerService.get_by_id(marker_id)
        if not marker:
            raise ValueError(f"Error getting marker with id={marker_id}")
        xml_data = OverpassService.overpass_related_nodes(marker.location)
        nodes = ScrapService.scrap_nodes(xml_data)
        return NodesToMarkersUpdaterManager.update_markers(nodes)
