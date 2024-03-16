from django.core.management.base import BaseCommand

from core.managers.markers_mainer import MarkerMainerCommandManager


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "scenario", choices=["main", "related"], help="Choose the scenario."
        )
        parser.add_argument(
            "--id", type=int, help="Specify the marker id for 'related' scenario."
        )
        parser.add_argument(
            "--pack",
            type=int,
            help="Specify the pack index for 'related batch' scenario.",
        )

    def handle(self, *args, **options):
        scenario = options["scenario"]
        marker_id = options.get("id")
        pack_index = options.get("pack")

        try:
            result = MarkerMainerCommandManager.handle_command(
                scenario, marker_id, pack_index
            )
            self.stderr.write(
                self.style.SUCCESS(
                    f"Scrapemrkers {scenario} id:{marker_id} pack:{pack_index} result: {result}"
                )
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
