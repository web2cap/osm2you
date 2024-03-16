import logging

from django.core.management import call_command
from django.db import transaction

from core.managers.nodes_to_markers_updater import NodesToMarkersUpdaterManager
from core.services.markers import MarkerService
from core.services.overpass import OverpassService
from core.services.related_markes_scrap import RelatedMarkerScrapService
from core.services.scrape import ScrapService
from core.tasks import run_scrap_markers_batch_related, run_scrap_markers_pack

logger = logging.getLogger(__name__)
overpass_service = OverpassService()


class MarkerMainerCommandManager:
    @staticmethod
    def handle_command(scenario, marker_id=None, pack_index=None):
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
                if pack_index:
                    return MarkerMainerScenarioManager.handle_related_pack_scenario(
                        pack_index
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
            pack_index = (
                free_pack_index
            ) = RelatedMarkerScrapService.get_next_free_pack_index()
            for marker_square in markers_by_squares:
                for markers in markers_by_squares[marker_square]:
                    RelatedMarkerScrapService.set_pack_index(markers, pack_index)
                    run_scrap_markers_pack.delay(pack_index)
                    pack_index += 1
            return f"Addad tasks for {pack_index - free_pack_index} packs"
        except Exception as e:
            logger.exception(f"Error occurred while handle_related_batch_scenario: {e}")

    @staticmethod
    def handle_related_pack_scenario(pack_index):
        try:
            markers = RelatedMarkerScrapService.get_by_pack_index(pack_index)
            with transaction.atomic():
                xml_data = overpass_service.overpass_batch_related_nodes(markers)
                nodes = ScrapService.scrap_nodes(xml_data)
                result = str(NodesToMarkersUpdaterManager.update_markers(nodes))
                RelatedMarkerScrapService.delete_pack(markers)
                logger.warning(f"Addad related pack {pack_index}: {result}")
            return result
        except Exception as e:
            logger.exception(f"Error occurred while handle_related_pack_scenario: {e}")
